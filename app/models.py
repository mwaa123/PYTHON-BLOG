from . import db
# from flask_login import UserMixin
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    # image_file =db.Column(db.String(225),default='default.jpg')
    # posts = db.relationship('Post',backref='author',lazy=True)

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
