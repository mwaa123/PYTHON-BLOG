from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, SelectField,TextAreaField,SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError



class PostForm(FlaskForm):   
    title = StringField ('title', validators=[Required()])
    content = TextAreaField('content', validators=[Required()]) 
    submit = SubmitField('post')