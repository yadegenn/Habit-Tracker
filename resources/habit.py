from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import HabitModel
from schemas import HabitSchema

blp = Blueprint("habit", __name__, description="Операции с привычками")

@blp.route("/habit")
class HabitView(MethodView):
    @blp.arguments(HabitSchema)
    @blp.response(201, HabitSchema)
    def post(self,habit_data):
        new_habit = HabitModel(**habit_data)

        db.session.add(new_habit)
        db.session.commit()

        return new_habit

    @blp.response(200, HabitSchema(many=True))
    def get(self):
        all_habit = HabitModel.query.all()

        return all_habit

@blp.route("/habit/<int:habit_id>")
class PickHabit(MethodView):
    @blp.response(200, HabitSchema)
    def get(self, habit_id):
        searched_habit = HabitModel.query.get_or_404(habit_id)

        return searched_habit

    def delete(self, habit_id):
        searched_habit = HabitModel.query.get_or_404(habit_id)
        db.session.delete(searched_habit)
        db.session.commit()
        return {"message": "Привычка успешно удалена"}