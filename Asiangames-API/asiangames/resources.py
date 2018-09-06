from copy import deepcopy

from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)
from flask import jsonify

from asiangames.models import User, Athlete, Country, Sport, Favourite
from asiangames.utils import get_id_by_name, get_favourite_names_by_ids
from asiangames.decorators import required_access_level
from asiangames.schemas import *


user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('email', help='Must enter a valid email', required=True)
user_login_parser.add_argument('password', help='Must enter a valid password', required=True)

user_registration_parser = deepcopy(user_login_parser)
user_registration_parser.add_argument('access_level', help='Must enter user level', required=True)


ACCESS_LEVELS = {
    'USER': 1,
    'ADMIN': 2
}

FAVOURITES_MAP = {
    'country': 1,
    'sport': 2,
    'athlete': 3
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

        return {
            'message': 'User with email {} was created'.format(data['email']),
            'access_token': create_access_token(identity=data['email']),
            'refresh_token': create_refresh_token(identity=data['email'])
        }


class UserLogin(Resource):

    def post(self):
        data = user_login_parser.parse_args()
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
    @required_access_level(ACCESS_LEVELS['ADMIN'])
    def get(self):
        current_user = get_jwt_identity()
        return {'hidden': 'Answer is 22', 'user_email': current_user}


class AthleteResource(Resource):

    def get(self, id):
        athlete_schema = AthleteSchema()
        athlete = Athlete.query.filter_by(_id=id).first()
        output = athlete_schema.dump(athlete).data

        return jsonify(output)


class AthleteListResource(Resource):

    def get(self):
        athlete_schema = AthleteSchema(many=True)
        athletes = Athlete.query.all()
        output = athlete_schema.dump(athletes).data

        return jsonify(output)


class AthleteFilterResource(Resource):

    def get(self, attribute, value):
        athlete_schema = AthleteSchema(many=True)

        if attribute == 'country':
            country_id = Country.query.filter_by(name=value).first()._id
            athletes = Athlete.query.filter_by(country_id=country_id).all()
            output = athlete_schema.dump(athletes).data
            return jsonify(output)

        elif attribute == 'sport':
            sport_record = Sport.query.filter_by(name=value).first()
            output = athlete_schema.dump(sport_record.athletes.all()).data
            return jsonify(output)

        elif attribute == 'weight':
            athletes = Athlete.query.filter_by(weight=int(value)).all()
            output = athlete_schema.dump(athletes).data
            return jsonify(output)

        elif attribute == 'height':
            athletes = Athlete.query.filter_by(height=int(value)).all()
            output = athlete_schema.dump(athletes).data
            return jsonify(output)

        elif attribute == 'age':
            athletes = Athlete.query.filter_by(age=int(value)).all()
            output = athlete_schema.dump(athletes).data
            return jsonify(output)


class ScheduleListResource(Resource):

    def get(self):
        schedule_schema = ScheduleSchema(many=True)
        schedules = Schedule.query.order_by(Schedule.daytime.desc()).all()
        output = schedule_schema.dump(schedules).data
        return jsonify(output)


class ScheduleFilterResource(Resource):

    def get(self, value):
        schedule_schema = ScheduleSchema(many=True)

        sport_record = Sport.query.filter_by(name=value).first()
        output = schedule_schema.dump(sport_record.schedules).data
        return output


class MedalsListResource(Resource):

    def get(self):
        medal_schema = SportCountryMedalsSchema(many=True)
        medals = SportCountryMedals.query.order_by(SportCountryMedals.gold.desc()).all()
        output = medal_schema.dump(medals).data
        return jsonify(output)


class MedalsFilterResource(Resource):

    def get(self, attribute, value):
        medal_schema = SportCountryMedalsSchema(many=True)

        if attribute == 'country':
            country_id = Country.query.filter_by(name=value).first()._id
            medals = SportCountryMedals.query.filter_by(country_id=country_id).order_by(SportCountryMedals.gold.desc()).all()
            output = medal_schema.dump(medals).data
            return jsonify(output)

        elif attribute == 'sport':
            sport_id = Sport.query.filter_by(name=value).first()._id
            medals = SportCountryMedals.query.filter_by(sport_id=sport_id).order_by(SportCountryMedals.gold.desc()).all()
            output = medal_schema.dump(medals).data
            return jsonify(output)


class FavouriteListResource(Resource):

    @jwt_required
    @required_access_level(ACCESS_LEVELS['USER'])
    def get(self, attribute):
        current_user_id = User.find_by_email(email=get_jwt_identity())._id

        if attribute == 'all':
            output_map = {}
            output_map['countries'] = get_favourite_names_by_ids(Favourite, current_user_id, Country, FAVOURITES_MAP['country'])
            output_map['sports'] = get_favourite_names_by_ids(Favourite, current_user_id, Sport, FAVOURITES_MAP['sport'])
            output_map['athletes'] = get_favourite_names_by_ids(Favourite, current_user_id, Athlete, FAVOURITES_MAP['athlete'])
            return jsonify(output_map)

        elif attribute == 'countries':
            return jsonify(get_favourite_names_by_ids(Favourite, current_user_id, Country, FAVOURITES_MAP['country']))

        elif attribute == 'sports':
            return jsonify(get_favourite_names_by_ids(Favourite, current_user_id, Sport, FAVOURITES_MAP['sport']))

        elif attribute == 'athletes':
            return jsonify(get_favourite_names_by_ids(Favourite, current_user_id, Athlete, FAVOURITES_MAP['athlete']))


class FavouriteFilterResource(Resource):

    @jwt_required
    @required_access_level(ACCESS_LEVELS['USER'])
    def post(self, attribute, value):
        current_user_id = User.find_by_email(email=get_jwt_identity())._id

        if attribute in FAVOURITES_MAP.keys():
            favourite_record = Favourite(favourite_object_id=value, favourite_entity_id=FAVOURITES_MAP[attribute],
                                         user_id=current_user_id)
            favourite_record.save_to_db()
            return {'message': '{} {} added to favourites'.format(attribute, value)}

        return {'message': 'Invalid attribute'}
