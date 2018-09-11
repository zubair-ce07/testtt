import os

view_controllers = "application.view_controllers"
template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")
url_mapping = "application.url_mapping"
DB_URL = os.path.join(os.path.dirname(__file__), "Recipes.db")
DB_MODELS = "application.database_models"
