from asiangames import app, restful_api, db
from asiangames import resources

if __name__ == '__main__':

    # user auth
    restful_api.add_resource(resources.UserRegistration, '/auth/registration')
    restful_api.add_resource(resources.UserLogin, '/auth/login')
    restful_api.add_resource(resources.TokenRefresh, '/auth/tokenrefresh')
    restful_api.add_resource(resources.MakeAdminSecret, '/auth/makeadmin')

    # athletes
    restful_api.add_resource(resources.AthleteListResource, '/athletes')
    restful_api.add_resource(resources.AthleteResource, '/athletes/<int:id>')
    restful_api.add_resource(resources.AthleteFilterResource, '/athletes/<string:attribute>/<int:value>')

    # schedules
    restful_api.add_resource(resources.ScheduleListResource, '/schedules')
    restful_api.add_resource(resources.ScheduleFilterResource, '/schedules/sport/<int:value>')

    # medals
    restful_api.add_resource(resources.MedalsListResource, '/medals')
    restful_api.add_resource(resources.MedalsFilterResource, '/medals/<string:attribute>/<int:value>')

    # favourites
    restful_api.add_resource(resources.FavouriteListResource, '/favourite/<string:attribute>')
    restful_api.add_resource(resources.FavouriteFilterResource, '/favourite/<string:attribute>/<string:value>')

    app.run()
