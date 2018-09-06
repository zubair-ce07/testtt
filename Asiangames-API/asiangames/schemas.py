from asiangames.models import Athlete, Sport, Country, Schedule, SportCountryMedals, Favourite
from asiangames import marshmallow_app


class SportSchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Sport


class CountrySchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Country


class AthleteSchema(marshmallow_app.ModelSchema):
    sports = marshmallow_app.Nested(SportSchema, only='name', many=True)
    country = marshmallow_app.Nested(CountrySchema, only='name')

    class Meta:
        model = Athlete


class ScheduleSchema(marshmallow_app.ModelSchema):
    sports = marshmallow_app.Nested(SportSchema, only='name')

    class Meta:
        model = Schedule


class SportCountryMedalsSchema(marshmallow_app.ModelSchema):
    sport = marshmallow_app.Nested(SportSchema, only='name')
    country = marshmallow_app.Nested(CountrySchema, only='name')

    class Meta:
        model = SportCountryMedals


class FavourtiteSchema(marshmallow_app.ModelSchema):
    sport = marshmallow_app.Nested(SportSchema, only='name')
    country = marshmallow_app.Nested(CountrySchema, only='name')
    athlete = marshmallow_app.Nested(Athlete, only='name')

    class Meta:
        model = Favourite
