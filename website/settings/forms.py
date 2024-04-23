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
    book_checkout = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class add_books_form(FlaskForm):
    book_name_add = StringField('Book Title', validators=[DataRequired()])
    book_genre_add = StringField('Book Genre', validators=[DataRequired()])
    submit = SubmitField('Add')

class delete_user_form(FlaskForm):
    username_del = StringField('Username', validators=[DataRequired()])
    admin_info = StringField('Admin Username', validators=[DataRequired()])
    submit = SubmitField('Delete')
