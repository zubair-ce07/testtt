![Asiangames API](https://instructobit.com/posts/111/post_preview_image(111).jpg)

Asiangames API presentes you all the information regarding:
1) Sports that were played
2) Countries that participated
3) Athletes
4) Medals won by each country in each sport

## Dependencies
1) [Flask](http://flask.pocoo.org/)
2) [Flask-RESTful](https://flask-restful.readthedocs.io/)
3) [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/)
4) [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)
5) [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/)

## Initial Setup
Update the following values in config.py
```bash
SECRET_KEY = 'TACHANKA'
JWT_SECRET_KEY = 'THATCHER'
MASTER_PASSWORD = 'ADMIN123' #will be used in secured routes
```

## Usage
After installing all the dependencies and  configuring config.py, run populate_db.py in the asiangames directory. It will populate the SQLite database for you.
Next, run run.py and your server will be hosted publically at **http://127.0.0.1:5000**

## Public Endpoints
```bash
GET      /athletes #returns all athletes
GET      /athletes/<int:id> #returns athlete with a particular id
GET      /athletes/country/<int:country_id> #returns all athletes from country with country_id
GET      /athletes/sport/<int:sport_id> #returns all athletes that are playing sport with sport_id
GET      /athletes/weight/<int:weight> #returns all athletes that weight equal to weight
GET      /athletes/height/<int:height> #returns all athletes that have height equal to height
GET      /athletes/age/<string:age> #returns all athletes that have age equal to age
```
```bash
GET      /schedules #returns all the schedules
GET      /schedules/sport/<string:sport_id> #returns all schedules of a particular sport with sport_id
```
```bash
GET      /medals #returns all the medals's records
GET      /medals/country/<int:country_id> #returns all medals won by the country with country_id and sorted by gold medals
GET      /medals/sport/<int:sport_id> #returns all the medals won by sport with sport_id
```

## User Authentication and Authorization

By becoming a user you can add Countries, Athletes and Sports to your favourites.
We use JSON web tokens for authentication.

**User Registration**

1) You need to add this header in the **POST** request:
```bash
key: Content-Type
value: application/json
```
2) In the body section you need to add the following
```bash
{
  "email": "uzair@gmail.com", #any valid email
  "password": "uzair", #a strong password
  "access_level": 1 #1 for USER, 2 for ADMIN
}
```
and then send the request to the following route
```bash
POST      /auth/register #to register yourself
```
It wil return you something like the following
```bash
{
    "message": "User with email uzair@gmail.com was registered",
    "access_token": <JWT_TOKEN>,
    "refresh_token": <JWT_TOKEN>
}
```
The access_token will be used for all the user routes that will be shown in a while.
Keep in mind that **access_token** will expire after 15 minutes and **refresh_token** will expire in 30 days.

**User Login**

1) You need to add this header in the **POST** request:
```bash
key: Content-Type
value: application/json
```
2) In the body section you need to add the following
```bash
{
  "email": "uzair@gmail.com", #your email with which you registered
  "password": "uzair", #your password with which you registered
}
```
and then send the request to the following route
```bash
POST      /auth/login #to login
```
It wil return you something like the following
```bash
{
    "message": "User with email uzair@gmail.com was registered",
    "access_token": <JWT_ACCESS_TOKEN>,
    "refresh_token": <JWT_REFRESH_TOKEN>
}
```

**Providing a User Admin Privileges**
```bash
PUT         /auth/makeadmin
```
add the following in body section
```bash
{
  "email": "uzair@gmail.com", #user's email
  "master_password": [MASTER_PASSWORD in config.py]
  
}
```

## User Privileges
Before making any request to the following routes, you need to do the following.

1) You need to add this header in the request:
```bash
key: Authorization
value: Bearer <JWT_ACCESS_TOKEN>
```
and now you can do these requests
```bash
POST    /favourite/country/<int: country_id> #to add country_id in your favourites
POST    /favourite/sport/<int:sport_id> #to add sport_id in your favourites
POST    /favourite/athlete/<int:athlete_id> #to add athlete with athlete_id in your favourites
GET     /favourite/all #to view all your favourites
GET     /favourite/countries #to get all your favourite countries
GET     /favourite/sports #to get all your favourite sports
GET     /favourite/athletes #to get all your favourite athletes
```
**That's pretty much it. Thanks alot :)**



