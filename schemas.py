from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PlainHabitSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    is_complete = fields.Bool(dump_only=True)
    streak = fields.Int(dump_only=True)
    weaky_goal = fields.Int(required=False)

class HabitSchema(PlainHabitSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)

class UserSchema(PlainUserSchema):
    habits = fields.List(fields.Nested(PlainHabitSchema(), dump_only=True))
