import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import HabitModel, UserModel, CompleteHabitsModel
from schemas import HabitSchema, HabitUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

blp = Blueprint("habit", __name__, description="Операции с привычками")

def filtered_habit(habit_id):
    id_user = int(get_jwt_identity())
    user = UserModel.query.get_or_404(id_user)
    searched_habit = HabitModel.query.filter(and_(HabitModel.user == user, HabitModel.id == habit_id)).first()
    if searched_habit == None:
        abort(404, message="Привычка не найдена или у вас к ней нет доступа")
    return searched_habit

def update_complete_status():
    user = UserModel.query.get_or_404(int(get_jwt_identity()))
    all_habits = HabitModel.query.filter(HabitModel.user == user)
    all_habits_ids = [i.id for i in all_habits]
    all_complete_habits = CompleteHabitsModel.query.filter(CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()
    sorted_list = []
    for i in all_complete_habits:
        srt_list_ids = [k['habit_id'] for k in sorted_list]
        if i.habit_id not in srt_list_ids:
            sorted_list.append({"id": i.id, "date": i.date, "habit_id": i.habit_id})
        else:
            there_index = srt_list_ids.index(i.habit_id)
            if i.date > sorted_list[there_index]['date']:
                sorted_list[there_index]['date'] = i.date
    for i in all_habits:
        if i.id not in [x['habit_id'] for x in sorted_list]:
            sorted_list.append({"date": datetime.now().date()-timedelta(days=1),"habit_id": i.id})
    for i in sorted_list:
        selected_habit = HabitModel.query.filter(and_(HabitModel.user == user, HabitModel.id == i["habit_id"])).first()
        if datetime.now(ZoneInfo("Europe/Moscow")).date()!=i["date"]:
            selected_habit.is_complete = False
        else:
            selected_habit.is_complete = True
        db.session.add(selected_habit)
        db.session.commit()


def update_streak_status():
    user = UserModel.query.get_or_404(int(get_jwt_identity()))
    all_habits = HabitModel.query.filter(and_(HabitModel.user == user, HabitModel.type!='weekly'))

    all_habits_ids = [i.id for i in all_habits]
    all_complete_habits = CompleteHabitsModel.query.filter(CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()
    all_complete_habits.sort(key=lambda x: x.date, reverse=True)
    all_complete_habits.sort(key=lambda x: x.habit_id)
    last_elements = []
    now_date = datetime.now().date()
    minus_days = 1
    for i in all_habits:
        if (i.is_complete == False):
            last_elements.append({"habit_id": i.id, "date": now_date, "streak": 0})
    for index, k in enumerate(all_complete_habits):
        if(k.habit_id not in [x['habit_id'] for x in last_elements]):
            minus_days = 1
            if(k.date!=now_date):
                last_elements.append({"habit_id": k.habit_id, "date": k.date, "streak": 0})
            else:

                last_elements.append({"habit_id": k.habit_id, "date": k.date, "streak": 1})
        else:
            if(k.date==now_date-timedelta(days=minus_days)):
                select_element = next((x for x in last_elements if x['habit_id'] == k.habit_id), None)
                if select_element:
                    select_element['date'] = k.date
                    select_element['streak'] = select_element['streak']+1
                    minus_days+=1
            else:
                select_element = next((x for x in last_elements if x['habit_id'] == k.habit_id), None)
                if select_element:
                    select_element['streak'] = select_element['streak']
    for i in last_elements:
        selected_habit = HabitModel.query.filter(and_(HabitModel.user == user, HabitModel.id == i["habit_id"])).first()
        selected_habit.streak = i['streak']
        db.session.add(selected_habit)
        db.session.commit()

def update_weekly_done():
    user = UserModel.query.get_or_404(int(get_jwt_identity()))
    all_habits = HabitModel.query.filter(and_(HabitModel.user == user, HabitModel.type == 'weekly'))

    all_habits_ids = [i.id for i in all_habits]
    all_complete_habits = CompleteHabitsModel.query.filter(CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()
    all_complete_habits.sort(key=lambda x: x.date, reverse=True)
    all_complete_habits.sort(key=lambda x: x.habit_id)

    temp_list = {
        #id: []
    }
    start_week = datetime.today().date() - timedelta(days=datetime.today().date().weekday())
    end_week = start_week+timedelta(days=6)
    for i in all_habits_ids:
        for k in all_complete_habits:
            if(i==k.habit_id):
                if start_week <= k.date <= end_week:
                    if k.habit_id not in temp_list:
                        temp_list[k.habit_id] = 1
                    else:
                        temp_list[k.habit_id] = temp_list[k.habit_id]+1
    for i in all_habits:
        if i.id not in list(temp_list.keys()):
            if(i.type=='weekly'):
                i.weekly_done = 0
    for i in list(temp_list.keys()):
        select_habit = next((x for x in all_habits if x.id==i), None)
        if select_habit:
            select_habit.weekly_done = temp_list[i]
            db.session.add(select_habit)
            db.session.commit()


@blp.route("/habit")
class HabitView(MethodView):
    @jwt_required()
    @blp.arguments(HabitSchema)
    @blp.response(201, HabitSchema)
    def post(self,habit_data):
        habit_data["user_id"] = int(get_jwt_identity())
        if(habit_data['type']=="weekly"):

            if not habit_data.get('weekly_goal'):
                abort(400, message="Для привычки с типом weekly обязательно нужно передавать weekly_goal")


        new_habit = HabitModel(**habit_data)
        if (habit_data['type'] == "weekly"):
            new_habit.weekly_done = 0
            new_habit.weekly_goal = 0

        db.session.add(new_habit)
        db.session.commit()

        return new_habit

    @jwt_required()
    @blp.response(200, HabitSchema(many=True))
    def get(self):
        update_complete_status()
        update_streak_status()
        update_weekly_done()

        id_user = int(get_jwt_identity())
        user = UserModel.query.get_or_404(id_user)
        all_habit = HabitModel.query.filter(HabitModel.user==user).all()
        return all_habit



@blp.route("/habit/<int:habit_id>")
class PickHabit(MethodView):
    @jwt_required()
    @blp.response(200, HabitSchema)
    def get(self, habit_id):
        update_complete_status()
        update_streak_status()
        update_weekly_done()
        searched_habit = filtered_habit(habit_id)
        if searched_habit == None:
            abort(404, message="Привычка не найдена или у вас к ней нет доступа")

        return searched_habit

    @jwt_required()
    def delete(self, habit_id):
        searched_habit = filtered_habit(habit_id)
        db.session.delete(searched_habit)
        db.session.commit()
        return {"message": "Привычка успешно удалена"}

    @jwt_required()
    @blp.arguments(HabitUpdateSchema)
    def patch(self, habit_data,habit_id):
        searched_habit = filtered_habit(habit_id)

        if(habit_data['is_complete'] and habit_data['is_complete']==True):
            user = UserModel.query.get_or_404(int(get_jwt_identity()))
            all_habits_ids = [i.id for i in HabitModel.query.filter(HabitModel.user == user)]
            all_complete_habits = CompleteHabitsModel.query.filter(
                CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()
            is_added_new_log = True
            for i in all_complete_habits:
                if i.habit_id==habit_id:
                    if i.date==datetime.now(ZoneInfo("Europe/Moscow")).date():
                        is_added_new_log = False
            if(is_added_new_log):
                new_log = CompleteHabitsModel(
                    date=datetime.now(ZoneInfo("Europe/Moscow")),
                    habit_id=habit_id
                )
                db.session.add(new_log)
                db.session.commit()

        elif (habit_data['is_complete'] == False):
            print(habit_data['is_complete'])
            user = UserModel.query.get_or_404(int(get_jwt_identity()))
            all_habits_ids = [i.id for i in HabitModel.query.filter(HabitModel.user == user)]
            all_complete_habits = CompleteHabitsModel.query.filter(
                CompleteHabitsModel.habit_id.in_(all_habits_ids)).all()
            is_delete_log = False
            id_delete = 0
            for i in all_complete_habits:
                if i.habit_id == habit_id:
                    if i.date == datetime.now(ZoneInfo("Europe/Moscow")).date():
                        is_delete_log = True
                        id_delete = i.id
            if (is_delete_log):
                log = CompleteHabitsModel.query.get_or_404(id_delete)
                db.session.delete(log)
                db.session.commit()
        searched_habit.is_complete = habit_data['is_complete']
        db.session.add(searched_habit)
        db.session.commit()
        return {"message": "Данные привычки обновлены"}