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

## Usage
After installing all the dependencies, run populate_db.py in the asiangames directory. It will populate the SQLite database for you.
Next, run run.py and your server will be hosted publically at **http://127.0.0.1/5000**

```bash
GET      /athletes/<int:id> #returns athlete with a particular id
GET      /athletes/all #returns all athletes
GET      /athletes/country/<string:_country> #returns all athletes from _country
GET      /athletes/sport/<string:_sport> #returns all athletes that are playing _sport
GET      /athletes/weight/<string:_weight> #returns all athletes that weight equal to _weight
GET      /athletes/height/<string:_height> #returns all athletes that have height equal to _height
GET      /athletes/age/<string:_age> #returns all athletes that have age equal to _age
```
```bash
GET      /schedules/all #returns all the schedules
GET      /schedules/sport/<string:_sport> #returns all schedules of a particular _sport
```
```bash
GET      /medals/all #returns all the medals's records
GET      /medals/country/<string:_country> #returns all medals won by the country and sorted by gold medals
GET      /medals/sport/<string:_sport> #returns all the medals won in _sport
```
```bash
GET      /medals/all #returns all the medals's records
GET      /medals/country/<string:_country> #returns all medals won by the country and sorted by gold medals
GET      /medals/sport/<string:_sport> #returns all the medals won in _sport
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
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzYwNDI4NjQsIm5iZiI6MTUzNjA0Mjg2NCwianRpIjoiOGE3ZDc4ZjMtMmFkMC00YThhLWI1NjctMDRmYmZmZjVhZjA4IiwiZXhwIjoxNTM2MDQzNzY0LCJpZGVudGl0eSI6InV6YWlyQGdtYWlsLmNvbSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.sdPaF-gRJ6eIaM4AoDU2L0EDp07_ggdTenCQtEdlnR4",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzYwNDI4NjQsIm5iZiI6MTUzNjA0Mjg2NCwianRpIjoiZjliYmYxYjctZjg3ZS00OGZhLTkxYjAtODE0MTBiYmZkNGZlIiwiZXhwIjoxNTM4NjM0ODY0LCJpZGVudGl0eSI6InV6YWlyQGdtYWlsLmNvbSIsInR5cGUiOiJyZWZyZXNoIn0.-VLbbxPlpjsCZHGfm65eomK4_bspcGFi3tTwxmi5_pM"
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
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzYwNDI4NjQsIm5iZiI6MTUzNjA0Mjg2NCwianRpIjoiOGE3ZDc4ZjMtMmFkMC00YThhLWI1NjctMDRmYmZmZjVhZjA4IiwiZXhwIjoxNTM2MDQzNzY0LCJpZGVudGl0eSI6InV6YWlyQGdtYWlsLmNvbSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.sdPaF-gRJ6eIaM4AoDU2L0EDp07_ggdTenCQtEdlnR4",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MzYwNDI4NjQsIm5iZiI6MTUzNjA0Mjg2NCwianRpIjoiZjliYmYxYjctZjg3ZS00OGZhLTkxYjAtODE0MTBiYmZkNGZlIiwiZXhwIjoxNTM4NjM0ODY0LCJpZGVudGl0eSI6InV6YWlyQGdtYWlsLmNvbSIsInR5cGUiOiJyZWZyZXNoIn0.-VLbbxPlpjsCZHGfm65eomK4_bspcGFi3tTwxmi5_pM"
}
```

## User Privileges
Before making any request to the following routes, you need to do the following.

1) You need to add this header in the request:
```bash
key: Authorization
value: Bearer <your_access_token>
```
and now you can do these requests
```bash
POST     /favourite/country/<string:_country> #to add _country in your favourites
POST     /favourite/country/<string:_sport> #to add _sport in your favourites
POST     /favourite/country/<string:_athlete_id> #to add athlete with _athlete_id in your favourites
GET      /favourite/all #to view all your favourites
GET     /favourite/countries #to get all your favourite countries
GET     /favourite/sports #to get all your favourite sports
GET     /favourite/athletes #to get all your favourite athletes
```
**That's pretty much it. Thanks alot :)**



