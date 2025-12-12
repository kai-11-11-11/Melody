# models.py
"""
Modelos SQLAlchemy para Melody.

Tablas:
 - interaction         -> registra interacciones/inputs de usuarios
 - emotion_alias       -> alias aprendidos por los usuarios (alias -> emoción + mensaje)
 - sound_preference    -> puntajes/feedback por sonido y emoción
 - emotion_stat        -> contadores simples por emoción

Compatible con MySQL (XAMPP) y SQLite. Use DATABASE_URL en app.py para configurar.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Interaction(db.Model):
    __tablename__ = "interaction"
    id = db.Column(db.Integer, primary_key=True)
    user_text = db.Column(db.Text, nullable=False)
    detected_emotion = db.Column(db.String(100), nullable=True)
    intensity = db.Column(db.String(50), nullable=True)
    # JSON type: supported in MySQL and SQLite (SQLAlchemy will fallback a TEXT if needed)
    sounds = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_text": self.user_text,
            "detected_emotion": self.detected_emotion,
            "intensity": self.intensity,
            "sounds": self.sounds,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class EmotionAlias(db.Model):
    __tablename__ = "emotion_alias"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(255), nullable=False, unique=True, index=True)
    emotion = db.Column(db.String(100), nullable=False, index=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def upsert(cls, alias: str, emotion: str, message: str = None):
        """
        Crea o actualiza un alias. Devuelve (obj, created_bool).
        """
        alias_norm = alias.strip().lower()
        inst = cls.query.filter_by(alias=alias_norm).first()
        if inst:
            inst.emotion = emotion
            inst.message = message
            db.session.add(inst)
            created = False
        else:
            inst = cls(alias=alias_norm, emotion=emotion, message=message)
            db.session.add(inst)
            created = True
        db.session.commit()
        return inst, created

class SoundPreference(db.Model):
    __tablename__ = "sound_preference"
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(100), nullable=False, index=True)
    sound_id = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('emotion', 'sound_id', name='_emotion_sound_uc'),
    )

    @classmethod
    def change_score(cls, emotion: str, sound_id: str, delta: int):
        """Incrementa (o decrementa) el score por (emotion, sound_id)."""
        emot = (emotion or "").strip()
        sid = (sound_id or "").strip()
        if not emot or not sid:
            raise ValueError("emotion and sound_id required")
        pref = cls.query.filter_by(emotion=emot, sound_id=sid).first()
        if not pref:
            pref = cls(emotion=emot, sound_id=sid, score=delta if delta>0 else 0 if delta==0 else delta)
            db.session.add(pref)
        else:
            pref.score = (pref.score or 0) + int(delta)
        db.session.commit()
        return pref

class EmotionStat(db.Model):
    __tablename__ = "emotion_stat"
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(100), nullable=False, unique=True)
    count = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @classmethod
    def increment(cls, emotion: str, by: int = 1):
        emo = (emotion or "").strip()
        if not emo:
            raise ValueError("emotion required")
        stat = cls.query.filter_by(emotion=emo).first()
        if not stat:
            stat = cls(emotion=emo, count=by)
            db.session.add(stat)
        else:
            stat.count = (stat.count or 0) + by
        db.session.commit()
        return stat
