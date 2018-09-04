from asiangames import app, api, db
import asiangames.resources as resources

if __name__ == '__main__':

    db.create_all()

    # user auth
    auth_route = '/auth/{}'
    api.add_resource(resources.UserRegistration, auth_route.format('registration'))
    api.add_resource(resources.UserLogin, auth_route.format('login'))
    api.add_resource(resources.TokenRefresh, auth_route.format('tokenrefresh'))

    # athletes
    api.add_resource(resources.AthleteResource, '/athletes/<int:id>')
    api.add_resource(resources.AthleteListResource, '/athletes/all')
    api.add_resource(resources.AthleteFilterResource, '/athletes/<string:attribute>/<string:value>')

    # schedules
    api.add_resource(resources.ScheduleListResource, '/schedules/all')
    api.add_resource(resources.ScheduleFilterResource, '/schedules/<string:attribute>/<string:value>')

    # medals
    api.add_resource(resources.MedalsListResource, '/medals/all')
    api.add_resource(resources.MedalsFilterResource, '/medals/<string:attribute>/<string:value>')

    # favourites
    api.add_resource(resources.FavouriteListResource, '/favourite/<string:attribute>')
    api.add_resource(resources.FavouriteFilterResource, '/favourite/<string:attribute>/<string:value>')

    app.run()
