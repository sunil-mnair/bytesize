from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField,FileRequired,FileAllowed

username_required = "Please provide a username"
password_required = "Please provide a password"

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(message=username_required)])
    password = PasswordField('Password',validators=[InputRequired(message=password_required)])
    remember = BooleanField(False)

class SignupForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(message=username_required)])
    password = PasswordField('Password',validators=[InputRequired(message=password_required)])

class UploadForm(FlaskForm):
    # pickle = FileField('Pickle', validators=[FileRequired(), FileAllowed(['pkl'], 'Pickle Files only!')])
    new_data = FileField('Data', validators=[FileRequired(), FileAllowed(['csv'])])