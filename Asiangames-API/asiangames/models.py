from passlib.hash import pbkdf2_sha256 as sha256

from asiangames import db


SportAthlete = db.Table(
    'sport_athlete',
    db.Column('athlete_id', db.Integer, db.ForeignKey('athlete._id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport._id'))
)


class Athlete(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img_url = db.Column(db.String(256))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    born_date = db.Column(db.String(16))
    born_city = db.Column(db.String(64))

    # many to mnay relationship with sport table
    sports = db.relationship('Sport', secondary=SportAthlete, backref=db.backref('athletes', lazy='dynamic'))

    # many to one relationship with country table
    country_id = db.Column(db.Integer, db.ForeignKey('country._id'))


class Sport(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    # one to many relationship with schedule table
    schedules = db.relationship('Schedule', backref=db.backref('sport'))


class SportCountryMedals(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country._id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('sport._id'))
    gold = db.Column(db.Integer)
    silver = db.Column(db.Integer)
    bronze = db.Column(db.Integer)

    # many to many relationship via association table pattern
    country = db.relationship('Country', backref=db.backref('medals'))  # parent
    sport = db.relationship('Sport', backref=db.backref('medals'))


class Country(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # one to many relationship with athlete table
    athletes = db.relationship('Athlete', backref=db.backref('country'))


class Schedule(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    daytime = db.Column(db.DateTime)
    phase = db.Column(db.String(64))
    event = db.Column(db.String(64))

    # one to many relationship with sport table
    sport_id = db.Column(db.Integer, db.ForeignKey('sport._id'))


class Favourite(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    favourite_object_id = db.Column(db.Integer)
    favourite_entity_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    access_level = db.Column(db.Integer, nullable=False, default=1)
    favorites = db.relationship('Favourite')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
