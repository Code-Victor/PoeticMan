from flask import flash
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     BooleanField, SubmitField,
                     DateField, SelectField)
from wtforms.validators import (DataRequired, Length, Optional,
                                Regexp, EqualTo, Email, AnyOf)
from wtforms import ValidationError
from ..models import User, Admin


class SignupForm(FlaskForm):
    """Represents the login form for users/admins."""

    email = StringField('Enter Your Email (for creating an admin account only)',
                        validators=[Optional(), Length(1, 255),
                                    Email()])
    username = StringField('What Would You Like Me To Call You? (Username)', validators=[
        DataRequired(), Length(3, 100),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Enter a New Password', validators=[
        DataRequired(), Length(8, 128),
    ])
    password2 = PasswordField('Confirm New Password',
                              validators=[
                                  DataRequired(),
                                  EqualTo('password',
                                          message='Passwords must match.')
                              ])
    birth_date = DateField('Enter Your Date of Birth',
                           validators=[DataRequired()])
    gender = SelectField('Enter Your Gender (for creating an admin account only)?', choices=[
        ('', '-- Select an option --'), ('female', 'Female'),
        ('male', 'Male'), ('others', 'Others')
    ], coerce=str, validators=[
        Optional(), AnyOf(['female', 'male', 'others'])
    ])
    is_admin = BooleanField('Admin Account?')
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        """Ensure the email passed does not already exists."""
        admin = Admin.query.filter_by(email=field.data).first()
        if admin:
            flash('Email already registered.', 'error')
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        """Ensure that the username passed does not already exists."""
        user = User.query.filter_by(username=field.data).first()
        if user:
            flash('Username already in use.')
            raise ValidationError('Username already in use.')
