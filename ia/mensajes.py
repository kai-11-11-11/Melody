# ia/mensajes.py
from typing import Dict, List, Optional
from .clasificador import detectar_emociones, calcular_intensidad, elegir_emocion_principal
from .reglas import sonidos_para_emocion
from .datos import SONIDOS, EMOCION_IMAGENES

def mensaje_motivacional(emocion: str, intensidad: str) -> str:
    base = "Recuerda: estás haciendo lo mejor que puedes ahora mismo."
    extras = {
        # ... (mantener sus mensajes existentes)
        "ansiedad": {
            "fuerte": "Respira profundo: 4 segundos in — 4 segundos out. No estás solo, esto pasará.",
            "medio": "Intenta centrarte en la respiración y en el sonido. Pequeños descansos ayudan.",
            "leve": "Notaste síntomas leves: tómate unos minutos para desconectar."
        },
        # ... el resto igual
    }
    if emocion in extras:
        return base + " " + extras[emocion].get(intensidad, "")
    return base

def _candidate_alias_from_text(texto: str) -> Optional[str]:
    """
    Extrae una sugerencia de alias:
    - si el texto es corto (<=30 chars) y tiene 1-3 palabras, devolverlo.
    - si es más largo, devolver la primera palabra destacada (normalizada).
    """
    if not texto:
        return None
    t = texto.strip()
    if len(t) <= 30 and len(t.split()) <= 3:
        return t.lower()
    # tomar primera palabra significativa
    first = t.split()[0].lower()
    return first

def construir_respuesta(texto_usuario: str) -> Dict:
    texto = (texto_usuario or "").strip()
    emociones = detectar_emociones(texto)
    intensidad = calcular_intensidad(texto)
    emocion_principal = elegir_emocion_principal(emociones)

    # Si no detecta, intentamos ver si existe un alias pre-registrado (DB lo gestiona
    # en reglas/otros; pero aquí dejamos la señal para la UI)
    need_label = False
    alias_hint = None

    if not emocion_principal:
        # proponer una palabra como alias para que el usuario la etiquete
        alias_hint = _candidate_alias_from_text(texto)
        need_label = True if alias_hint else False

    sonidos_ids = sonidos_para_emocion(emocion_principal, intensidad) if emocion_principal else ["frecuencia_432hz", "lluvia_suave"]

    if emocion_principal is None:
        analisis = "No pude detectar claramente cómo te sientes."
    else:
        analisis = f"Detecté que tu emoción principal es **{emocion_principal.replace('_',' ')}** (intensidad: {intensidad})."

    detalle_sonidos = []
    for sid in sonidos_ids:
        meta = SONIDOS.get(sid, {})
        nombre = meta.get("nombre", sid)
        uso = meta.get("uso", "")
        detalle_sonidos.append({"id": sid, "nombre": nombre, "uso": uso})

    mensaje = analisis + "\n\nTe recomiendo escuchar lo siguiente:\n"
    for d in detalle_sonidos:
        mensaje += f"- {d['nombre']} ({d['id']}) — {d['uso']}\n"

    motivacion = mensaje_motivacional(emocion_principal, intensidad)
    mensaje += "\n" + motivacion + "\n"

    imagen_emocion = EMOCION_IMAGENES.get(emocion_principal) if emocion_principal else EMOCION_IMAGENES.get("default")

    return {
        "emociones_detectadas": emociones,
        "emocion_principal": emocion_principal,
        "intensidad": intensidad,
        "sonidos": detalle_sonidos,
        "mensaje": mensaje,
        "motivacion": motivacion,
        "imagen_emocion": imagen_emocion,
        # señales para UI si necesita etiquetado humano
        "need_label": need_label,
        "alias_hint": alias_hint
    }
