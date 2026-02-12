from zoneinfo import ZoneInfo

from db import db
from schemas import TypeOfHabits
from zoneinfo import  ZoneInfo
from datetime import datetime

class HabitModel(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum(TypeOfHabits), nullable=False)
    is_complete = db.Column(db.Boolean, default=False,nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    weakly_goal = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.Date, nullable=True, default=datetime.now(ZoneInfo("Europe/Moscow")).date())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="habits")