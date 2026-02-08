from db import db
class HabitModel(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    is_complete = db.Column(db.Boolean, default=False,nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    weakly_goal = db.Column(db.Integer, nullable=True)
    user = db.relationship("UserModel", back_populates="habits")