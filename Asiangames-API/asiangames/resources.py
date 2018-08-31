from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)
from flask import jsonify

from asiangames.models import User, Athlete
from asiangames.decorators import required_access_level
from asiangames.schemas import *


user_registration_parser = reqparse.RequestParser()
user_registration_parser.add_argument('email', help='Must enter a valid email', required=True)
user_registration_parser.add_argument('password', help='Must enter a valid password', required=True)
user_registration_parser.add_argument('access_level', help='Must enter user level', required=True)

access_levels = {
    'USER': 1,
    'ADMIN': 2
}


class UserRegistration(Resource):

    def post(self):
        data = user_registration_parser.parse_args()

        if User.find_by_email(data['email']):
            return {'message': 'User with email {} already exists'.format(data['email'])}

        new_user = User(
            email=data['email'],
            password=User.generate_hash(data['password']),
            access_level=data['access_level']
        )

        new_user.save_to_db()
        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        return {
            'message': 'User with email {} was created'.format(data['email']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class UserLogin(Resource):

    def post(self):
        data = user_registration_parser.parse_args()
        current_user = User.find_by_email(email=data['email'])

        if current_user:
            if User.verify_hash(data['password'], current_user.password):

                access_token = create_access_token(identity=data['email'])
                refresh_token = create_refresh_token(identity=data['email'])
                return {
                    'message': 'User with email {} was logged in'.format(data['email']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }

            return {'message': 'Invalid credentials'}
        else:
            return {'message': 'User with email {} does not exist'.format(data['email'])}


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class SecretResourse(Resource):

    @jwt_required
    @required_access_level(access_levels['ADMIN'])
    def get(self):
        current_user = get_jwt_identity()
        return {'hidden': 'Answer is 22', 'user_email': current_user}


class AthletesResource(Resource):

    def get(self, id):
        athlete_schema = AthleteSchema()
        athlete = Athlete.query.filter_by(_id=id).first()
        output = athlete_schema.dump(athlete).data

        return jsonify({'athlete': output})

