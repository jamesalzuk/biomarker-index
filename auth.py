from models import User
from passlib.hash import sha256_crypt
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
from app import db
from datetime import datetime

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()
        # read from database to find the user and then check the password
        user = User.query.filter_by(email=data['email']).first()
        
        if user and safe_str_cmp(user.password, data['password']):
            # when authenticated, return a fresh access token and a refresh token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {"message": "Invalid Credentials!"}, 401

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
        )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
        )

    def post(self):
        data = self.parser.parse_args()
        # read from database to find the user and then check the password
        user = User(
        email=data['email'],
        password=data['password'],
        registered_on=datetime.now()
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created"}, 200