from framework.database_handler import BaseModel
from peewee import CharField

models = [
    "Recipe",
]


class Recipe(BaseModel):
    name = CharField(max_length=50)
    difficulty = CharField(max_length=10)
    description = CharField()
    ingredients = CharField()

    class Meta:
        table_name = "recipes"
