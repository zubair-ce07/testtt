from asiangames import app, restful_api, db
from asiangames import resources

if __name__ == '__main__':

    # user auth
    auth_route = '/auth/{}'
    restful_api.add_resource(resources.UserRegistration, auth_route.format('registration'))
    restful_api.add_resource(resources.UserLogin, auth_route.format('login'))
    restful_api.add_resource(resources.TokenRefresh, auth_route.format('tokenrefresh'))

    # athletes
    athlete_route = '/athletes/{}/{}'
    restful_api.add_resource(resources.AthleteResource, athlete_route.format('<int:id>', ''))
    restful_api.add_resource(resources.AthleteListResource, athlete_route.format('all', ''))
    restful_api.add_resource(resources.AthleteFilterResource, athlete_route.format('<string:attribute>', '<string:value>'))

    # schedules
    schedules_route = '/schedules/{}/{}'
    restful_api.add_resource(resources.ScheduleListResource, schedules_route.format('all'))
    restful_api.add_resource(resources.ScheduleFilterResource, schedules_route.format('<string:value>', ''))

    # medals
    medals_route = '/medals/{}/{}'
    restful_api.add_resource(resources.MedalsListResource, medals_route.format('all', ''))
    restful_api.add_resource(resources.MedalsFilterResource, medals_route.format('<string:attribute>', '/<string:value>'))

    # favourites
    favourite_route = '/favourite/{}/{}'
    restful_api.add_resource(resources.FavouriteListResource, favourite_route.format('<string:attribute>', ''))
    restful_api.add_resource(resources.FavouriteFilterResource, favourite_route.format('<string:attribute>', '<int:value>'))

    app.run()
