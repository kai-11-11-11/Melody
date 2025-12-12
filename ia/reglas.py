# ia/reglas.py
from typing import List
from .datos import RECOMENDACIONES_SONIDO

def sonidos_para_emocion(emocion: str, intensidad: str = "medio") -> List[str]:
    if not emocion:
        return ["frecuencia_432hz", "lluvia_suave"]

    base = RECOMENDACIONES_SONIDO.get(emocion, ["frecuencia_432hz"])

    # intentar priorizar por preferencias guardadas en DB (si están presentes)
    try:
        # import dinámico para evitar circular imports al arrancar la app
        from models import SoundPreference
        prefs = SoundPreference.query.filter_by(emocion=emocion).order_by(SoundPreference.score.desc()).all()
        if prefs:
            prefs_ids = [p.sonido_id for p in prefs if p.sonido_id in base]
            resto = [s for s in base if s not in prefs_ids]
            base = prefs_ids + resto
    except Exception:
        # ignorar si no hay DB disponible o si ocurre cualquier error
        pass

    if intensidad == "fuerte":
        prior = [s for s in base if "frecuencia" in s or "cuenco" in s or "respiracion" in s]
        resto = [s for s in base if s not in prior]
        return prior + resto

    if intensidad == "leve":
        prior = [s for s in base if s in ["lluvia_suave", "bosque_tranquilo", "noche_grillos", "rio_constante"]]
        resto = [s for s in base if s not in prior]
        return prior + resto

    return base
