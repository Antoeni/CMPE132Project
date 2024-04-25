
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
class delete_user_page(FlaskForm):
    deleted_username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Delete')

class add_books_form(FlaskForm):
    book_name_add = StringField('Book Title', validators=[DataRequired()])
    book_genre_add = StringField('Book Genre', validators=[DataRequired()])
    submit = SubmitField('Add')

class admin_add_books_form(FlaskForm):
    admin_book_name_add = StringField('Book Title', validators=[DataRequired()])
    admin_book_genre_add = StringField('Book Genre', validators=[DataRequired()])
    submit = SubmitField('Add')

class login_page(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign In')
class checkout_book_page (FlaskForm):
    book_checkout = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class sign_up(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField(
        'Role',
        validators=[DataRequired()],
        choices=[
            ('choose', 'Choose...'),
            ('student/general', 'Student/General'),
            ('librarian', 'Librarian'),
            ('admin', 'Admin'),
        ],
        default='student'
    )
    submit = SubmitField('Register')