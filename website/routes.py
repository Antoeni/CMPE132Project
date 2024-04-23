import requests
from website.settings.roles import User, Delete_user, checkout_books_role, data_book
from website.settings.forms import login_form, sign_up_form, delete_user_form, checkout_book_form, add_books_form
from website import myapp_obj, db
from flask import flash, url_for, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta


#sets up the database
@myapp_obj.before_request
def create_db():
    db.create_all()
#creates the routing to the home page
@myapp_obj.route("/")
def home_page():
    return render_template('home_page.html')

@myapp_obj.route('/login/', methods=['GET', 'POST'])
def login():
    logout_user()
    form = login_form()
    if form.validate_on_submit():
        if form.submit.data:
            user_login = User.query.filter_by(username=form.username.data).first()
            if user_login and user_login.check_password(form.password.data):
                login_user(user_login)
                if user_login.role == 'admin':
                    return redirect('/home_admin/')
                elif user_login.role == 'librarian':
                    return redirect('/home_librarian/')
                else:
                    return redirect('/general_home/')
            else:
                flash("Username or Password is incorrect.")
                return render_template('login.html', form=form)
        if form.guest.data:
            return redirect('/browse/')
    return render_template('login.html', form=form)

@myapp_obj.route('/logout/')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/')

@myapp_obj.route('/register/', methods=['POST', 'GET'])
def register():
    logout_user()
    form = sign_up_form()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists.")
        else:
            user = User(username=form.username.data, password=form.password.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            if user.role == 'admin':
                return redirect('/home_admin/')
            elif user.role == 'user':
                return redirect('/general_home/')
            elif user.role == 'librarian':
                return redirect('/home_librarian/')
            elif user.role =='choose':
                flash("Choose a role.")
    return render_template('signup.html', form=form)

#Gives the routing for the general users and students
@myapp_obj.route('/general_home/', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('general_home.html', user=current_user)

@myapp_obj.route('/checkout/', methods=['GET', 'POST'])
@login_required
def checkout_book():
    form = checkout_book_form()
    if form.validate_on_submit():
        user_id = current_user.id
        book_ttl = data_book.query.filter_by(book_title=form.book_checkout.data).first()
        if book_ttl is None:
            flash("Book not found.")
        else:
            checkout = checkout_books_role(username=current_user.username, bookname=book_ttl.book_title)
            db.session.add(checkout)
            db.session.delete(book_ttl)
            db.session.commit()
    else:
        flash('invalid input')
    books = data_book.query.all()
    return render_template('checkout_books.html', form=form, books=books)


@myapp_obj.route('/browse/', methods=['POST', 'GET'])
def browse():
    books = data_book.query.all()
    return render_template('browse.html', user=current_user, books=books)
#Gives the routing for the admins and their pages
@myapp_obj.route('/home_admin/', methods=['POST', 'GET'])
@login_required
def home_admin():
    return render_template('home_admin.html', user=current_user)
@myapp_obj.route('/admin_database', methods=['POST', 'GET'])
@login_required
def admin_database():
    login_info = User.query.all()
    books = data_book.query.all()
    delete = Delete_user.query.all()
    return render_template('admin_database.html', login_info=login_info, books=books, deletes=delete)

@myapp_obj.route('/delete/', methods=['POST', 'GET'])
@login_required
def delete_user():
    form = delete_user_form()
    if form.validate_on_submit():
        if form.admin_info.data == current_user.username:
            deleted_user = User.query.filter_by(username=form.username_del.data).first()
            if deleted_user:
                user_delete = Delete_user(admin_username=current_user.username, deleted_user=deleted_user.username, delete_time=datetime.now(), admin_id=current_user.id, user_id=deleted_user.id)
                db.session.add(user_delete)
                db.session.delete(deleted_user)
                db.session.commit()
                flash("User has been deleted.")
                return redirect('/delete/')
            else:
                flash("Username does not exist.")
        else:
            flash("Admin Login Incorrect.")
    return render_template('delete_user.html', form=form)
#Gives the routing for the librarians and their commands
@myapp_obj.route('/home_librarian/', methods=['POST', 'GET'])
@login_required
def home_librarian():
    return render_template('home_librarian.html', user=current_user)

@myapp_obj.route('/library_books/', methods=['POST', 'GET'])
def library_books():
    books = data_book.query.all()
    return render_template('librarian_view.html', books=books)

@myapp_obj.route('/add_books/', methods=['GET', 'POST'])
@login_required
def add_books_route():
    form = add_books_form()
    if form.validate_on_submit():
        book_info = data_book(book_title=form.book_name_add.data, book_genre=form.book_genre_add.data)
        db.session.add(book_info)
        db.session.commit()
        flash('Book added', 'success')
        return redirect(url_for('add_books_route'))
    return render_template('add_book.html', form=form)

@myapp_obj.route('/books/', methods=['POST', 'GET'])
def books():
    books = data_book.query.all()
    return render_template('browse.html', books=books)

