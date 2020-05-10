from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    image_file =db.Column(db.String(225),default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)

    @property
    def password(self):
        raise AttributeError('Denied')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)



    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key = True) 
    title = db.Column(db.String(255),index=True)
    date_posted = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    content = db.Column(db.Text,index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'Post {self.title}'