from db import db

class CompleteHabitsModel(db.Model):
    __tablename__ = 'complete_habits'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    habit_id = db.Column(db.ForeignKey("habits.id"), nullable=False)