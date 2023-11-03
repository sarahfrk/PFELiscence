from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    id = StringField('Matricule', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    posts=StringField('Role',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    id = StringField('Matricule', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    posts=StringField('Role',validators=[DataRequired()])
    submit = SubmitField('Sing up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AjoutAnimal(FlaskForm):
    codeAnimal = StringField('Code Animal', validators=[DataRequired()])
    espece = StringField('Espèce', validators=[DataRequired()])
    famille = StringField('famille', validators=[DataRequired()])
    embranchement = StringField('Emranchement', validators=[DataRequired()])
    race = StringField('Race', validators=[DataRequired()])
    couleur = StringField('Couleur', validators=[DataRequired()])
    pelage = StringField('Pelage', validators=[DataRequired()])
    sexe = StringField('Sexe', validators=[DataRequired()])
    poids = FloatField('Poids', validators=[DataRequired()])
    taille = FloatField('Taille', validators=[DataRequired()])
    origine = StringField('Origine', validators=[DataRequired()])
    DateNais = DateField('La Date et Le Lieu De Naissance', validators=[DataRequired()])
    DateDeses = DateField('Date décès', validators=[DataRequired()])
    SignePart = StringField('Signe Particulie', validators=[DataRequired()])
    NumZone = IntegerField('Num Zone', validators=[DataRequired()])
    NumEnclo = IntegerField('Num Enclos', validators=[DataRequired()])

    def validate_username(self, codeAnimal):
        animal = Animal.query.filter_by(codeAnimal=codeAnimal.data).first()
        if animal is not None:
            raise ValidationError('Ce code est déja réservé')


class ChercherAnimal(FlaskForm):
    codeAnimal = StringField('Code Animal', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    id=IntegerField('id', validators=[DataRequired()])
    nom= StringField('nom', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    message=StringField('message',validators=[DataRequired()])
    submit = SubmitField('envoyer')
