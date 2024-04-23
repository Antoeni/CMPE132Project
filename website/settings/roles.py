from flask_login import UserMixin
from website import login,db
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Delete user, this will set up the information for when we delete the user later
class delete_roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(20), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deleted_user = db.Column(db.String(20), nullable=False)
    #this will create a relationship between the user's info, which the foreign key to access it is the admin key.
    admin = db.relationship('User', foreign_keys=[admin_id], backref='deleted_users', uselist=False)

#User information, this will set up the information about the user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    #this will create a relationship between the deleted roles
    deleted = db.relationship('delete_roles', backref='admin_user', foreign_keys='delete_roles.admin_id')
    #password hashing here
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


#Book Checkout Information, which, it will just look for the book name
class checkout_books_role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(20), nullable=True)

#this will set up the information about the book, which contains the genres and book title
class data_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(20),nullable=False)
    book_genre = db.Column(db.String(20), nullable=False)

