from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from wtforms import TextAreaField
from wtforms.validators import Length
from app.models import User
from wtforms import IntegerField

# Formular für die Anmeldung
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Leeres Formular, z.B. für "Follow"/"Unfollow"-Aktionen
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Formular zur Bearbeitung des Benutzerprofils
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

# Formular für das Erstellen eines neuen Posts
class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

# Formular für die Registrierung eines neuen Benutzers
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Überprüft, ob der Benutzername bereits verwendet wird
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    # Überprüft, ob die E-Mail-Adresse bereits verwendet wird
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Formular für die Bewertung mit einer Zahl zwischen 1 und 10
class RatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Submit')
