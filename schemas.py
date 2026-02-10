from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainHabitSchema(Schema):
    id = fields.Int(dump_only=True, required=False)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    is_complete = fields.Bool(dump_only=True, required=False)
    streak = fields.Int(dump_only=True, required=False)
    weaky_goal = fields.Int(required=False)

class HabitSchema(PlainHabitSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True, required=False)

class UserSchema(PlainUserSchema):
    habits = fields.List(fields.Nested(PlainHabitSchema(), dump_only=True))
