from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Email, Length
from app import User # There is a table of user in my project. You can change it to your table name or delete this import
from forms.validators import Unique, AuthorizationName, AuthorizationPassword
import email_validator
from app.settings import get_string_contain
from app.website_processing import get_form_choices

DATA_EMPTY_MESSAGE = "You send empty field!!!"


class LoginForm(FlaskForm):
    """ 
    Form for login page.
    """
    username = StringField(validators=[InputRequired("Fill this field!"), AuthorizationName(User)])
    password = PasswordField(validators=[InputRequired("Fill this field!"), AuthorizationPassword(User)])
    remember_me = BooleanField("Запам'ятати мене")
    submit = SubmitField("Залогінитись")


class RegisterForm(FlaskForm):
    """
    Form for register page.
    """
    username = StringField(validators=[InputRequired("Обов'язкове до заповнення!"), Unique(User, User.username), Length(min=2, max=12)])
    email = EmailField(validators=[Email("Невірна пошта!"), Unique(User, User.email), InputRequired("Обов'язкове до заповнення!")])
    password = PasswordField(validators=[InputRequired("Обов'язкове до заповнення!"), Length(min=8, max=36)])
    password_reply = PasswordField(validators=[EqualTo('password', message="Паролі не співпадають!"), InputRequired("Обов'язкове до заповнення!"), Length(min=8, max=36)])
    submit = SubmitField("Зареєструватися")


class SettingsForm(FlaskForm):
    language = SelectField("Виберіть мову", choices=get_form_choices("languages"))
    submit = SubmitField("Прийняти")


class CoinsForm(FlaskForm):
    submit = SubmitField("Здобути коіни")


class ConsoleForm(FlaskForm):
    command = StringField(render_kw={"placeholder": "Write command"})
    submit = SubmitField("send")
