from asiangames import app, api
import asiangames.routes, asiangames.resources as resources

if __name__ == '__main__':
    auth_route = '/auth/{}'
    api.add_resource(resources.UserRegistration, auth_route.format('registration'))
    api.add_resource(resources.UserLogin, auth_route.format('login'))

    app.run()
