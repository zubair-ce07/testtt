from asiangames.models import Athlete, Sport, Country
from asiangames import marshmallow_app


class SportSchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Sport


class CountrySchema(marshmallow_app.ModelSchema):
    class Meta:
        model = Country


class AthleteSchema(marshmallow_app.ModelSchema):
    sports = marshmallow_app.Nested(SportSchema, only='name', many=True)
    country = marshmallow_app.Nested(CountrySchema, only='name', many=True)

    class Meta:
        model = Athlete
