from marshmallow import Schema, fields
from enum import Enum

class TypeOfHabits(str, Enum):
    daily = "daily",
    weekly = "weekly"

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainHabitSchema(Schema):
    id = fields.Int(dump_only=True, required=False)
    name = fields.Str(required=True)
    type = fields.Enum(TypeOfHabits, required=True)
    is_complete = fields.Bool(dump_only=True, required=False)
    streak = fields.Int(dump_only=True, required=False)
    weaky_goal = fields.Int(dump_only=True, required=False)
    created_at = fields.Date(dump_only=True, required=False)

class HabitSchema(PlainHabitSchema):
    user_id = fields.Int(required=False, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True, required=False)

class UserSchema(PlainUserSchema):
    habits = fields.List(fields.Nested(PlainHabitSchema(), dump_only=True))

class HabitUpdateSchema(Schema):
    is_complete = fields.Bool(required=True)

class CompleteHabits(Schema):
    id = fields.Int(required=False, dump_only=True)
    date = fields.Date(required=True)
    habit_id = fields.Int(required=True)