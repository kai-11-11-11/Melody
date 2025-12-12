# ia/datos.py
from typing import Dict, List

# EMOCIONES: más frases, errores comunes y variantes coloquiales
EMOCIONES: Dict[str, List[str]] = {
    "ansiedad": [
        "ansioso", "ansiosa", "ansiedad", "nervioso", "nerviosa",
        "me tiembla", "me preocupa", "preocupado", "preocupada",
        "no puedo parar de pensar", "pensamientos acelerados", "corazon acelerado",
        "me siento inquieto", "me siento nervioso", "tengo ansiedad",
        "angoja", "angustia", "angustiado", "angustiada",
        "me pongo nervioso", "me entra nervios", "me sudan las manos"
    ],
    "panico": [
        "pánico", "panico", "voy a tener un ataque", "me estoy ahogando",
        "siento que me desmayo", "no puedo respirar", "ataque de pánico",
        "siento que me muero"
    ],
    "estres": [
        "estresado", "estresada", "estrés", "estres", "agobiado", "agobiada",
        "sobrecarga", "muchas cosas", "presión", "no doy abasto", "no doy a basto",
        "colapso", "me estresa"
    ],
    "tristeza": [
        "triste", "tristeza", "deprimido", "deprimida", "lloro", "llorando",
        "me siento vacío", "me siento vacio", "sin ganas", "melancolía", "melancolia",
        "nostalgia", "estoy mal", "me siento mal", "mal", "me siento decaido",
        "decaido", "decaída", "decaido", "muy triste", "me duele el alma"
    ],
    "duelo": [
        "me murió", "me murio", "falleció", "fallecio", "he perdido a", "duelo", "no puedo superar"
    ],
    "soledad": [
        "solo", "sola", "me siento solo", "me siento sola", "aislado", "aislada",
        "nadie me entiende", "me siento abandonado"
    ],
    "cansancio_mental": [
        "agotado", "agotada", "mentalmente cansado", "no me concentro",
        "saturado", "quemado", "burnout", "fatiga mental", "exhausto", "sin fuerzas"
    ],
    "insomnio": [
        "no puedo dormir", "insomnio", "me desvelo", "no duermo", "inquietud nocturna",
        "no pego ojo", "no pego ojo hoy"
    ],
    "irritacion": [
        "irritado", "irritada", "molesto", "molesta", "furioso", "frustrado",
        "enojado", "enfadado", "me enoja", "me da rabia"
    ],
    "aburrimiento": [
        "aburrido", "aburrida", "sin nada que hacer", "me aburro", "aburri"
    ],
    "desmotivacion": [
        "sin ganas", "no tengo ganas", "desmotivado", "desmotivada",
        "no quiero hacer nada", "apagado", "sin energía", "sin energia"
    ],
    "falta_de_foco": [
        "no me concentro", "me distraigo", "no puedo enfocarme", "disperso",
        "me cuesta concentrarme", "me cuesta enfocarme"
    ],
    "alegria": [
        "feliz", "contento", "contenta", "alegre", "emocionado", "entusiasmado",
        "genial", "muy bien"
    ],
    "confusion": [
        "confundido", "confundida", "no sé qué hacer", "no se que hacer",
        "no sé qué hacer", "no entiendo", "desorientado", "perdido", "estoy perdido"
    ]
}

# INTENSIDAD: añadí tokens y símbolos que incrementan intensidad
INTENSIDAD_PALABRAS = {
    "alta": [
        "muy", "demasiado", "extremadamente", "intenso", "terrible", "totalmente",
        "no puedo", "siempre", "todo el tiempo", "constante", "a diario",
        "muchísimo", "muchisimo", "MUY", "!!!", "!!", "!!!"
    ],
    "media": [
        "bastante", "algo", "un poco", "algo de", "medio", "moderado", "algo mucho","aveces"
    ],
    "baja": [
        "un poco", "ligero", "leve", "ocasionalmente", "casi nunca"
    ]
}

# PRIORIDADES (misma lógica)
PRIORIDADES = [
    "panico", "ansiedad", "estres", "insomnio", "irritacion",
    "tristeza", "duelo", "soledad", "cansancio_mental",
    "desmotivacion", "falta_de_foco", "aburrimiento", "confusion", "alegria"
]

# RECOMENDACIONES (idénticas, puedes añadir más IDs de archivos)
RECOMENDACIONES_SONIDO: Dict[str, List[str]] = {
    "ansiedad": ["frecuencia_432hz", "cuenco_tibetano_grave", "lluvia_suave", "om_profundo"],
    "panico": ["respiracion_guided", "frecuencia_432hz", "cuenco_tibetano_grave"],
    "estres": ["frecuencia_528hz", "handpan_suave", "bosque_tranquilo"],
    "tristeza": ["frecuencia_417hz", "flauta_suave", "bosque_tranquilo"],
    "duelo": ["flauta_suave", "cuenco_cuarzo", "pad_etereo_lento"],
    "soledad": ["coros_suaves", "bosque_tranquilo", "lluvia_suave"],
    "cansancio_mental": ["dron_do", "rio_constante", "frecuencia_528hz"],
    "insomnio": ["frecuencia_432hz", "olas_mar_suaves", "noche_grillos", "cuenco_cuarzo"],
    "irritacion": ["campanas_tibetanas_suaves", "dron_re", "respiracion_guided"],
    "aburrimiento": ["handpan_melodico", "pad_ascendente", "frecuencia_741hz"],
    "desmotivacion": ["frecuencia_741hz", "handpan_suave", "campanas_tibetanas"],
    "falta_de_foco": ["frecuencia_528hz", "rio_constante", "dron_do"],
    "confusion": ["om_profundo", "pad_etereo_lento", "flauta_suave"],
    "alegria": ["handpan_vibrante", "campanas_tibetanas_brillantes", "pad_luz"]
}

# SONIDOS: metadatos
SONIDOS: Dict[str, Dict[str, str]] = {
    "frecuencia_432hz": {"nombre": "Frecuencia 432Hz", "duracion": "5-30min", "uso": "relajación profunda"},
    "frecuencia_528hz": {"nombre": "Frecuencia 528Hz", "duracion": "5-30min", "uso": "sanación/armonía"},
    "frecuencia_417hz": {"nombre": "Frecuencia 417Hz", "duracion": "5-20min", "uso": "limpieza emocional"},
    "frecuencia_741hz": {"nombre": "Frecuencia 741Hz", "duracion": "5-20min", "uso": "claridad mental"},
    "cuenco_tibetano_grave": {"nombre": "Cuenco tibetano (grave)", "duracion": "1-10min", "uso": "grounding"},
    "cuenco_cuarzo": {"nombre": "Cuenco de cuarzo", "duracion": "1-8min", "uso": "relajación alta frecuencia"},
    "handpan_suave": {"nombre": "Handpan suave", "duracion": "2-10min", "uso": "melodía calmante"},
    "handpan_melodico": {"nombre": "Handpan melódico", "duracion": "2-10min", "uso": "estimular creatividad"},
    "bosque_tranquilo": {"nombre": "Bosque tranquilo", "duracion": "10-60min", "uso": "ambiental"},
    "lluvia_suave": {"nombre": "Lluvia ligera", "duracion": "10-60min", "uso": "ambiente reconfortante"},
    "olas_mar_suaves": {"nombre": "Olas suaves", "duracion": "10-60min", "uso": "relajación/insomnio"},
    "noche_grillos": {"nombre": "Noche con grillos", "duracion": "10-60min", "uso": "insomnio/relajación"},
    "rio_constante": {"nombre": "Río/arroyo", "duracion": "10-60min", "uso": "concentración y calma"},
    "dron_do": {"nombre": "Dron en DO", "duracion": "5-30min", "uso": "anclaje tonal"},
    "dron_re": {"nombre": "Dron en RE", "duracion": "5-30min", "uso": "claridad"},
    "om_profundo": {"nombre": "Tono OM profundo", "duracion": "5-30min", "uso": "meditación"},
    "pad_etereo_lento": {"nombre": "Pad etéreo lento", "duracion": "5-30min", "uso": "ambient"},
    "pad_ascendente": {"nombre": "Pad ascendente", "duracion": "1-5min", "uso": "transición"},
    "pad_luz": {"nombre": "Pad luminiscente", "duracion": "2-8min", "uso": "euforia suave"},
    "campanas_tibetanas_suaves": {"nombre": "Campanas tibetanas (suaves)", "duracion": "1-5min", "uso": "transición"},
    "campanas_tibetanas_brillantes": {"nombre": "Campanas tibetanas (brillantes)", "duracion": "1-5min", "uso": "alegría"},
    "respiracion_guided": {"nombre": "Guía de respiración (audio)", "duracion": "3-10min", "uso": "calmar panico/ansiedad"},
    "coros_suaves": {"nombre": "Coros suaves", "duracion": "5-20min", "uso": "apoyo emocional"}
}
# al final de ia/datos.py (añada estas líneas)
EMOCION_IMAGENES = {
    "ansiedad": "/static/images/emotions/ansiedad.jpg",
    "panico": "/static/images/emotions/panico.jpg",
    "estres": "/static/images/emotions/estres.jpg",
    "tristeza": "/static/images/emotions/tristeza.jpg",
    "duelo": "/static/images/emotions/duelo.jpg",
    "soledad": "/static/images/emotions/soledad.jpg",
    "cansancio_mental": "/static/images/emotions/cansancio_mental.jpg",
    "insomnio": "/static/images/emotions/insomnio.jpg",
    "irritacion": "/static/images/emotions/irritacion.jpg",
    "aburrimiento": "/static/images/emotions/aburrimiento.jpg",
    "desmotivacion": "/static/images/emotions/desmotivacion.jpg",
    "falta_de_foco": "/static/images/emotions/falta_de_foco.jpg",
    "confusion": "/static/images/emotions/confusion.jpg",
    "alegria": "/static/images/emotions/alegria.jpg",
    # fallback
    "default": "/static/images/emotions/default.jpg"
}


# Helpers de export/import (idénticos)
import json, os
def guardar_json(filepath: str):
    payload = {
        "EMOCIONES": EMOCIONES,
        "INTENSIDAD_PALABRAS": INTENSIDAD_PALABRAS,
        "PRIORIDADES": PRIORIDADES,
        "RECOMENDACIONES_SONIDO": RECOMENDACIONES_SONIDO,
        "SONIDOS": SONIDOS
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def cargar_json(filepath: str):
    global EMOCIONES, INTENSIDAD_PALABRAS, PRIORIDADES, RECOMENDACIONES_SONIDO, SONIDOS
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        payload = json.load(f)
    EMOCIONES = payload.get("EMOCIONES", EMOCIONES)
    INTENSIDAD_PALABRAS = payload.get("INTENSIDAD_PALABRAS", INTENSIDAD_PALABRAS)
    PRIORIDADES = payload.get("PRIORIDADES", PRIORIDADES)
    RECOMENDACIONES_SONIDO = payload.get("RECOMENDACIONES_SONIDO", RECOMENDACIONES_SONIDO)
    SONIDOS = payload.get("SONIDOS", SONIDOS)

def todos_los_ids_de_sonido() -> List[str]:
    return list(SONIDOS.keys())
