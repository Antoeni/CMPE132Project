
from website import login,db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


#Delete user:
class delete_roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(20), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deleted_user = db.Column(db.String(20), nullable=False)
    delete_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    admin = db.relationship('User', foreign_keys=[admin_id], backref='deleted_users', uselist=False)

#User information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    deleted = db.relationship('delete_roles', backref='admin_user', foreign_keys='delete_roles.admin_id')
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def set_password(self, password):
        self.password = generate_password_hash(password)

#Book Checkout Information
class checkout_books_role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=True)
    bookname = db.Column(db.String(20), nullable=True)

#Database information
class data_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(20),nullable=False)
    book_genre = db.Column(db.String(20), nullable=False)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
