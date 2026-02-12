from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

from models import UserModel, HabitModel, CompleteHabitsModel
from schemas import CompleteHabits
blp = Blueprint("complete_habits", __name__, description="Операции с таблицой завершенных привычек")

@blp.route("/habit-completions")
class HabitCompletions(MethodView):

    @jwt_required()
    @blp.response(200, CompleteHabits(many=True))
    def get(self):

        user = UserModel.query.get_or_404(int(get_jwt_identity()))
        all_habits_ids = [i.id for i in HabitModel.query.filter(HabitModel.user==user)]
        return CompleteHabitsModel.query.filter(CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()