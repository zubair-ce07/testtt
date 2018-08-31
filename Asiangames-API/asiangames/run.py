from asiangames import app, api, db
import asiangames.routes, asiangames.resources as resources

if __name__ == '__main__':

    db.create_all()

    auth_route = '/auth/{}'
    api.add_resource(resources.UserRegistration, auth_route.format('registration'))
    api.add_resource(resources.UserLogin, auth_route.format('login'))
    api.add_resource(resources.AthletesResource, '/athletes/<int:id>')

    app.run()
