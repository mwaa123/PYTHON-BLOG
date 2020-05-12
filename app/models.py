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
    image_file =db.Column(db.String(225))
    profile_pic_path = db.Column(db.String(255))
    bio = db.Column(db.String(225))
    comment = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    post = db.relationship('Post',backref='author',lazy=True)

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
    comment = db.relationship('Comment', backref='title', lazy='dynamic')
    def __repr__(self):
        return f'Post {self.title}'


class  Comment(db.Model):
    __tablename__="comments"
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comment(cls,blog_id):
        comment=Comment.query.filter_by(post_id=post_id).all()
        return comment
