from models import *
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(60))
    avatar = db.Column(db.String(50))
    created_time = db.Column(db.String(30), default=0)
    blogs = db.relationship('Blog', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = '/static/images/avatar.jpg'
        self.created_time = format_time(int(time.time()))

    def valid_register(self):
        return 1 < len(self.username) < 16 and 2 < len(self.password) < 16

    def valid_login(self, u):
        return check_password_hash(self.password, u.password)

    def hash_password(self, password):
        self.password = generate_password_hash(password)
        # print(self.password)
