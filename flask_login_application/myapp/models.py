from werkzeug.security import check_password_hash,generate_password_hash
from myapp import db,login_manager
from flask_login import UserMixin
"""provides general implementations required 
    by LoginManager
"""


@login_manager.user_loader
def load_user(id):
    """this function helps flask_login to retrieve a user provided the id
    """
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """This class is used for managing 'users'
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
