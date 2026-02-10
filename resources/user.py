from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models.user import UserModel
from schemas import PlainUserSchema, UserSchema

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

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username==user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            # refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, messsage="Недействительные данные")

@blp.route("/user")
class AllUser(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        all_models = UserModel.query.all()
        return all_models
