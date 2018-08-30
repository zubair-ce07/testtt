from flask_restful import Resource, reqparse


email_pass_parser = reqparse.RequestParser()
email_pass_parser.add_argument('email', help='Must enter a valid email', required=True)
email_pass_parser.add_argument('password', help='Must enter a valid password', required=True)


class UserRegistration(Resource):

    def post(self):
        data = email_pass_parser.parse_args()
        return data


class UserLogin(Resource):

    def post(self):
        data = email_pass_parser.parse_args()
        return data


class UserLogoutAccess(Resource):

    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):

    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
