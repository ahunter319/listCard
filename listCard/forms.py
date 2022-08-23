from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
from listCard.models import User


# User Forms
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please try another.')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("That email already exists. Please choose a different one.")

    username = StringField(label="Username", validators=[InputRequired(), Length(min=2, max=30)])
    email = StringField(label="Email", validators=[InputRequired(), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(), Length(min=8)])
    confirm = PasswordField(label="Confirm Password", validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    curr_pass = PasswordField(label="Current Password", validators=[InputRequired()])
    new_pass = PasswordField(label="New Password", validators=[InputRequired()])
    conf_new_pass = PasswordField(label="Confirm New Password", validators=[InputRequired()])
    submit = SubmitField("Confirm")


class DeleteAccountForm(FlaskForm):
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField("Delete Account")


class SetThemeForm(FlaskForm):
    theme = SelectField(label="Theme", choices=[('classic', 'Classic'), ('dark', 'Dark'), ('mint', 'Mint')])
    submit = SubmitField(label="Set Theme")


# Project Forms
class AddProjectForm(FlaskForm):

    project_name = StringField(label="Project Name", validators=[InputRequired(), Length(min=4, max=30)])
    project_description = StringField(label="Description", validators=[InputRequired(), Length(max=100)])
    submit = SubmitField(label="Add Project")


class AddItemForm(FlaskForm):

    item_name = StringField(label="Item Name", validators=[InputRequired()])
    submit = SubmitField(label="Add to List")


class AddCommentForm(FlaskForm):

    comment = StringField(label="Comments")
    submit = SubmitField(label="Save")
