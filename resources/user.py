from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from db import db
from models.user import UserModel
from schemas import PlainUserSchema

blp = Blueprint("user", __name__, description="Операции с пользователями")

@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        new_user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password'])
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Пользователь успешно зарегистрирован"}, 201