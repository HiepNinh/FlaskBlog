from flask import request
from flask_restful import Resource
from databases.models import User
from datetime import timedelta
from extensions import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


class LoginApi(Resource):
   def post(self):
       body = request.get_json()
       user = User.query.filter_by(email=body.get('email')).first()
       if user and bcrypt.check_password_hash(user.password, body.get('password')):
           expires = timedelta(days=7)
           access_token = create_access_token(identity=str(user.id), expires_delta=expires)
           return {'token': access_token}, 200
       return {'error': 'Email or password invalid'}, 401
   
    
class UsersApi(Resource):
    @jwt_required
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 5, type=int)
        users = [result.serialized for result in User.query.paginate(page=page, per_page=page_size).items]
        return users, 200
    
    
class UserApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        return user.serialized, 200
