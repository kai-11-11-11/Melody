# ia/clasificador.py
from typing import List
import re
from .datos import EMOCIONES, INTENSIDAD_PALABRAS, PRIORIDADES

def _normalizar(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.lower()
    # reemplazar acentos básicos
    reemplazos = {
        "á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n"
    }
    for k,v in reemplazos.items():
        texto = texto.replace(k, v)
    # eliminar caracteres extraños excepto signos
    texto = re.sub(r"[^a-z0-9ñáéíóúü\\s¡!\\?\\.,']", " ", texto)
    # compactar espacios
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def detectar_emociones(texto: str) -> List[str]:
    texto_l = _normalizar(texto)
    encontradas = []
    for etiqueta, palabras in EMOCIONES.items():
        for p in palabras:
            p_norm = _normalizar(p)
            if p_norm in texto_l:
                encontradas.append(etiqueta)
                break
    return encontradas

def calcular_intensidad(texto: str) -> str:
    texto_l = texto or ""
    texto_norm = _normalizar(texto_l)
    score = 0

    # palabras de intensidad (alta/media/baja)
    for p in INTENSIDAD_PALABRAS.get("alta", []):
        if _normalizar(p) in texto_norm:
            score += 2
    for p in INTENSIDAD_PALABRAS.get("media", []):
        if _normalizar(p) in texto_norm:
            score += 1
    for p in INTENSIDAD_PALABRAS.get("baja", []):
        if _normalizar(p) in texto_norm:
            score -= 1

    # indicios extra: mayúsculas (todo en MAYÚSCULAS -> aumenta), repetición de letras, signos múltiples
    if texto_l.strip() == texto_l.strip().upper() and re.search(r"[A-ZÁÉÍÓÚÑ]", texto_l):
        score += 2
    # repetición de letras: "muyyyy", "soportaaaar"
    if re.search(r"(.)\1{3,}", texto_l):  # misma letra 4+ veces
        score += 1
    # múltiples signos de exclamación o pregunta
    if re.search(r"[!]{2,}", texto_l) or re.search(r"[?]{2,}", texto_l):
        score += 1

    # normalizar a leve/medio/fuerte
    if score >= 3:
        return "fuerte"
    elif score >= 1:
        return "medio"
    else:
        return "leve"

def elegir_emocion_principal(emociones: List[str]) -> str:
    if not emociones:
        return None
    for p in PRIORIDADES:
        if p in emociones:
            return p
    return emociones[0]
