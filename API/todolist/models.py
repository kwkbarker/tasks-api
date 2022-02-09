from todolist import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
    
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    tasks = db.relationship('Task', backref='created_by_user', lazy=True)

    def __str__(self) -> str:
        return self.username

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=128), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False)
    importance = db.Column(db.String(length=12), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    done = db.Column(db.Boolean, default=False, nullable=False) 

    def __repr__(self):
        return self.title

    # creates JSON-friendly format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'importance': self.importance
        }

# # add db views to admin page
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Task, db.session))


# # prints SQL commands for cloud sql table creation
# from sqlalchemy.schema import CreateTable
# print(CreateTable(User.__table__))
# print(CreateTable(Task.__table__))