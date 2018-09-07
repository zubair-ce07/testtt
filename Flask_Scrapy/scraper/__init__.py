from flask import Flask

from . import auth, item, update_progress
from .database import db_session, init_db

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///scrap.db'
)

init_db()
app.register_blueprint(auth.bp)
app.register_blueprint(item.bp)
app.register_blueprint(update_progress.bp)
app.add_url_rule('/', endpoint='index')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
