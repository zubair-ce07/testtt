This project was Create with [Flask](http://flask.pocoo.org/).

# Flicker App

A simple Flask Flicker app that allow the Users performs the following tasks:

* `Sign Up` Users
* `Sign In` User
* `Upload` Photos
* `Add` tags to Photos
* `Follow` User can follow other Users
*  `UnFollow` User Can Un follow the following Users
* `Home` Where Logged in User Can See Following User's Photo, Public Photo and Logged In User's Photos
* `Profile` User Can See Profile of other User's
* `Search Users ` User Can Search Users by Username
* `Search Posts` User can Search Posts by tags
* `Delete Photos`  User can delete his uploaded Photos
* `Likes`   User can Like/ Unlike Photos
* `Add Comments` User Can Comment on Photos
* `Delete Comments` User Can delete his comments
* `Detail View` User can see Detail View of Photo which includes (Photo's Likes and Comments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.

### Prerequisites

Need to have Python installed.

### Installing

First of all clone the project and change to that directory.

```
git clone https://github.com/arbisoft/the-lab.git
cd ./flicker
```

Then to install the required modules

```
pip install -r requirements.txt
```

### Starting

You've got project all setup, now all you need to do is start the development server, that will run on port 5000 by default.

```
python app.py
```
