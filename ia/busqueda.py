# ia/busqueda.py
"""
Funciones de búsqueda/optimización simples para combinar sonidos.
Por ejemplo: dado un conjunto de sonidos y una duración máxima, busca una combinación.
"""

from typing import List, Tuple, Dict

def combinar_sonidos_greedy(sonidos: List[Dict], duracion_max: float) -> List[Dict]:
    """
    Ejemplo trivial: ordena por 'prioridad' (si existe) y añade hasta llenar duracion.
    Cada 'sonido' puede ser dict con {'id','duracion_estimada','prioridad'}.
    """
    seleccion = []
    tiempo = 0.0
    # fallback: suponer duracion_estimada en minutos en metadata
    sonidos_sorted = sorted(sonidos, key=lambda s: s.get('prioridad', 0), reverse=True)
    for s in sonidos_sorted:
        d = float(s.get('duracion_estimada', 5))
        if tiempo + d <= duracion_max:
            seleccion.append(s)
            tiempo += d
    return seleccion

# Aquí puedes añadir búsqueda A*, backtracking, etc., cuando lo necesites.
