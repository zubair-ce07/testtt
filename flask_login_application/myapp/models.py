from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from myapp import db, login_manager

"""provides general implementations required 
    by LoginManager
"""


@login_manager.user_loader
def load_user(id):
    """Return a User instance provided the user id."""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """This class is used for managing 'users'.

    Methods :
    set_password(self, password) -- set a password hash for a user.
    check_password(self, password) -- check a given password against password hash for a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
