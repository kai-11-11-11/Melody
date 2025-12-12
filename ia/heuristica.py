# ia/heuristica.py
"""
Heurísticas para puntuar combinaciones de sonidos o para ponderar emociones.
Ejemplo: scoring simple que combina intensidad emocional con 'afinidad' de sonido.
"""

from typing import Dict, List

def score_sonido_para_emocion(sonido_meta: Dict, emocion: str, intensidad: str) -> float:
    """
    Devuelve un score numérico. Implementación base:
    - si el uso del sonido contiene palabras clave de la emoción, sube score.
    - ajustar por intensidad (p. ej. priorizar frecuencias cuando intensidad==fuerte).
    """
    score = 0.0
    uso = (sonido_meta.get('uso') or "").lower()
    if emocion and emocion in uso:
        score += 2.0
    if intensidad == "fuerte" and ("frecuencia" in sonido_meta.get("nombre","").lower() or "cuenco" in sonido_meta.get("nombre","").lower()):
        score += 1.5
    # Añade más reglas según necesites
    return score

def ordenar_sonidos_por_heuristica(sonidos_meta: List[Dict], emocion: str, intensidad: str) -> List[Dict]:
    ranked = sorted(sonidos_meta, key=lambda s: score_sonido_para_emocion(s, emocion, intensidad), reverse=True)
    return ranked
