from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, SelectField,TextAreaField,SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):   
    title = StringField ('title', validators=[Required()])
    content = TextAreaField('content', validators=[Required()]) 
    submit = SubmitField('post')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Required(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Required(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')   

class UpdateProfile(FlaskForm):
    bio = TextAreaField('About you',validators=[Required()])
    submit = SubmitField('submit')
class Comments(FlaskForm):
    comment=TextAreaField('Write Comment', validators=[Required()])
    submit=SubmitField('Comment')