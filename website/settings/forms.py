from flask_wtf import FlaskForm
from wtforms import StringField,  HiddenField, SelectField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class login_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class sign_up_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField(
        'Role',
        validators=[DataRequired()],
        choices=[
            ('choose', 'Choose...'),
            ('user', 'Student/General'),
            ('librarian', 'Librarian'),
            ('admin', 'Admin'),
        ],
        # Set the default value here or remove it to have no default value
        default='student'
    )
    submit = SubmitField('Register')

class checkout_book_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    book_title = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class edit_profile_form(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Edit')

class add_books_to_library(FlaskForm):
    book_name = StringField('Book Title', validators=[DataRequired()])
    book_genere = StringField('Book Genere', validators=[DataRequired()])
    book_available = BooleanField('Available')
    submit = SubmitField('Add')

class delete_user_form(FlaskForm):
    username_del = StringField('Username', validators=[DataRequired()])
    admin_cred = StringField('Admin Username', validators=[DataRequired()])
    reason_del = TextAreaField('Reason for Deletion', validators=[DataRequired()])
    submit = SubmitField('Delete')
