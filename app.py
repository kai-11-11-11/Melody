# app.py
import os
import json
from flask import Flask, render_template, request, jsonify
from ia.mensajes import construir_respuesta
from ia import datos as datos_mod
from ia.datos import PRIORIDADES  # para pasar al template

# IMPORT MODELS (asegúrese que models.py está en la misma carpeta que app.py)
from models import db, Interaction, EmotionAlias, SoundPreference, EmotionStat

app = Flask(__name__)

# --- CONFIG DB: Si quiere usar MySQL (XAMPP), configure la variable de entorno DATABASE_URL
# Ejemplo para XAMPP local: mysql+pymysql://root:password@127.0.0.1/melody_db
# Si no existe, por defecto se usa sqlite local data.sqlite
DATABASE_URL = os.environ.get("DATABASE_URL")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, "data.sqlite")
if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Crea tablas si no existen
    db.create_all()

# Intentar cargar persistencia del archivo (si existe)
try:
    datos_mod.cargar_todo()
except Exception:
    pass

# CARGAR ALIASES EN MEMORIA: sincronizar DB -> EMOCIONES en ia/datos (para detección rápida)
def load_aliases_into_memory():
    try:
        aliases = EmotionAlias.query.all()
        if not aliases:
            return
        # para cada alias, agregar alias a EMOCIONES[emoción]
        for a in aliases:
            emo = a.emotion  # en models.py el campo se llama 'emotion'
            alias = a.alias
            em_map = datos_mod.EMOCIONES
            if emo not in em_map:
                em_map[emo] = []
            if alias not in em_map[emo]:
                em_map[emo].append(alias)
        # opcional: persistir backup local
        try:
            datos_mod.guardar_todo()
        except Exception:
            pass
    except Exception as e:
        print("Warning load_aliases_into_memory:", e)

with app.app_context():
    load_aliases_into_memory()

# Guardar interacción (adaptado a los nombres de columnas de models.py)
def guardar_interaccion_db(texto, respuesta):
    try:
        inter = Interaction(
            user_text=texto,
            detected_emotion=respuesta.get("emocion_principal"),
            intensity=respuesta.get("intensidad"),
            sounds=[s["id"] for s in respuesta.get("sonidos", [])]  # JSON column
        )
        db.session.add(inter)

        # actualizar EmotionStat usando el helper disponible
        emo = respuesta.get("emocion_principal")
        if emo:
            try:
                # use classmethod increment si existe
                EmotionStat.increment(emo)
            except Exception:
                # fallback manual
                stat = EmotionStat.query.filter_by(emotion=emo).first()
                if not stat:
                    stat = EmotionStat(emotion=emo, count=1)
                    db.session.add(stat)
                else:
                    stat.count = (stat.count or 0) + 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error guardando en DB:", e)

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    texto = ''
    imagen_emocion = None
    if request.method == 'POST':
        texto = request.form.get('texto_usuario', '').strip()
        respuesta = construir_respuesta(texto)
        # Guardar en BD
        guardar_interaccion_db(texto, respuesta)
        # decidir imagen: si respuesta incluye imagen_emocion preferir esa
        imagen_emocion = respuesta.get("imagen_emocion")
    # pasar PRIORIDADES para el modal/selector
    return render_template('index.html', respuesta=respuesta, texto=texto, imagen_emocion=imagen_emocion, PRIORIDADES=PRIORIDADES)

# Endpoint para guardar un alias etiquetado por usuario
@app.route('/label', methods=['POST'])
def label_alias():
    """
    JSON esperado:
    {
      "alias": "luto",
      "target_emotion": "duelo",
      "message": "Mensaje que quiero que se muestre a quien usa 'luto'"
    }
    """
    payload = request.get_json() or {}
    alias = (payload.get("alias") or "").strip().lower()
    target = (payload.get("target_emotion") or "").strip()
    message = payload.get("message") or None

    if not alias or not target:
        return jsonify({"ok": False, "error": "alias y target_emotion son requeridos"}), 400

    try:
        # usar el helper upsert definido en models.EmotionAlias si está disponible
        try:
            obj, created = EmotionAlias.upsert(alias=alias, emotion=target, message=message)
        except Exception:
            # fallback manual si upsert no existe
            existing = EmotionAlias.query.filter_by(alias=alias).first()
            if existing:
                existing.emotion = target
                existing.message = message
                db.session.add(existing)
                created = False
                obj = existing
            else:
                obj = EmotionAlias(alias=alias, emotion=target, message=message)
                db.session.add(obj)
                created = True
            db.session.commit()

        # actualizar memoria en ia.datos para detección inmediata
        em_map = datos_mod.EMOCIONES
        if target not in em_map:
            em_map[target] = []
        if alias not in em_map[target]:
            em_map[target].append(alias)

        # persistir a archivo (opcional/backup)
        try:
            datos_mod.guardar_todo()
        except Exception:
            pass

        return jsonify({"ok": True, "message": f"Alias '{alias}' mapeado a '{target}'.", "created": bool(created)})
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

# endpoint para recuperar el mensaje personalizado de un alias (opcional)
@app.route('/alias-info', methods=['GET'])
def alias_info():
    alias = (request.args.get("alias") or "").strip().lower()
    if not alias:
        return jsonify({"ok": False, "error": "alias requerido"}), 400
    a = EmotionAlias.query.filter_by(alias=alias).first()
    if not a:
        return jsonify({"ok": True, "found": False}), 200
    return jsonify({"ok": True, "found": True, "alias": a.alias, "emotion": a.emotion, "message": a.message})

# endpoint para recibir feedback sobre sonidos (mantener compatibilidad)
@app.route('/feedback', methods=['POST'])
def feedback():
    payload = request.get_json() or {}
    emocion = payload.get("emocion")
    sonido = payload.get("sonido_id")
    accion = payload.get("accion")  # 'positivo' or 'negativo' or 'aceptar'
    if not emocion or not sonido:
        return jsonify({"ok": False, "error": "missing data"}), 400
    try:
        # ajustar score simple usando SoundPreference.change_score helper si existe
        delta = 0
        if accion == "positivo":
            delta = 1
        elif accion == "negativo":
            delta = -1
        elif accion == "aceptar":
            delta = 2
        try:
            pref = SoundPreference.change_score(emotion=emocion, sound_id=sonido, delta=delta)
        except Exception:
            # fallback manual
            pref = SoundPreference.query.filter_by(emotion=emocion, sound_id=sonido).first()
            if not pref:
                pref = SoundPreference(emotion=emocion, sound_id=sonido, score=max(delta, 0))
                db.session.add(pref)
            else:
                pref.score = (pref.score or 0) + int(delta)
            db.session.commit()
        return jsonify({"ok": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Si quiere escuchar en todas las interfaces en desarrollo (ej. pruebas en VM), puede usar host='0.0.0.0'
    app.run(debug=True)
