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

    # many to many relationship with country table
    sport_countries = db.relationship('SportCountryMedals')

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
    country = db.relationship('Country', backref=db.backref('sports'))  # parent
    sport = db.relationship('Sport', backref=db.backref('countries'))


class Country(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # many to many relationship via association table pattern
    country_sports = db.relationship('SportCountryMedals')

    # one to many relationship with athlete table
    athletes = db.relationship('Athlete')


class Schedule(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    daytime = db.Column(db.DateTime)
    phase = db.Column(db.String(64))
    event = db.Column(db.String(64))

    # one to many relationship with sport table
    sport_id = db.Column(db.Integer, db.ForeignKey('sport._id'))
