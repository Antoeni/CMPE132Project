import requests
from website.settings.models import User, Rent_books, Book_data, Delete_user
from website.settings.forms import login_form, sign_up_form, delete_user_form, checkout_book_form, add_books_to_library
from flask import  flash, redirect, render_template, url_for
from flask_login import login_user, logout_user,  current_user, login_required
from datetime import datetime, timedelta
from website import myapp_obj, db

@myapp_obj.before_request
def create_db():
    db.create_all()

@myapp_obj.route("/")
def home_page():
    return render_template('home_page.html')

@myapp_obj.route('/login/', methods=['GET', 'POST'])
def login():
    logout_user()
    form = login_form()
    if form.validate_on_submit():
        if form.submit.data:
            site_user = User.query.filter_by(username=form.username.data).first()
            if site_user and site_user.check_password(form.password.data):
                login_user(site_user)
                if site_user.role == 'admin':
                    return redirect('/home_admin/')
                elif site_user.role == 'librarian':
                    return redirect('/home_librarian/')
                else:
                    return redirect('/general_home/')
            else:
                flash("Username or Password is incorrect. Register for account if needed.")
                return render_template('login.html', form=form)
        if form.guest.data:
            return redirect('/browse/')
    return render_template('login.html', form=form)

@myapp_obj.route('/logout/')
def logout():
    logout_user()
    flash("You are logged out.")
    return redirect('/')

@myapp_obj.route('/register/', methods=['POST', 'GET'])
def register():
    logout_user()
    form = sign_up_form()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Choose another one.")
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
                flash("Select a role.")
    return render_template('signup.html', form=form)

@myapp_obj.route('/general_home/', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('general_home.html', user=current_user)

@myapp_obj.route('/home_admin/', methods=['POST', 'GET'])
@login_required
def home_admin():
    return render_template('home_admin.html', user=current_user)

@myapp_obj.route('/home_librarian/', methods=['POST', 'GET'])
@login_required
def home_lib():
    return render_template('home_librarian.html', user=current_user)

@myapp_obj.route('/browse/', methods=['POST', 'GET'])
def browse():
    books = Book_data.query.all()
    return render_template('browse.html', user=current_user, books=books)
    
@myapp_obj.route('/delete/', methods=['POST', 'GET'])
@login_required
def delete_user():
    form = delete_user_form()
    if form.validate_on_submit():
        if form.admin_cred.data == current_user.username:
            user_to_delete = User.query.filter_by(username=form.username_del.data).first()
            if user_to_delete:
                user_delete = Delete_user(admin_username=current_user.username, deleted_user=user_to_delete.username, delete_time=datetime.now(), admin_id=current_user.id, user_id=user_to_delete.id) 
                db.session.add(user_delete)
                db.session.delete(user_to_delete)
                db.session.commit()
                flash("User has been deleted.")
                return redirect('/delete/')
            else:
                flash("Username does not exist.")
        else:
            flash("Admin credential incorrect.")
    return render_template('delete_user.html', form=form)

@myapp_obj.route('/checkout/', methods=['GET', 'POST'])
@login_required
def checkout_book():
    form = checkout_book_form()
    if form.validate_on_submit():
        user_id = current_user.id
        book_title = Book_data.query.filter_by(book_ttl=form.book_title.data).first()
        print(book_title)
        if book_title == None:
            flash("Book not found.")
        else:
            checkout = Rent_books(username=current_user.username, bookname=book_title.book_ttl, returndate=datetime.now()+timedelta(days=7))
            db.session.add(checkout)
            db.session.delete(book_title)
            db.session.commit()
    else:
        flash('invalid input')
    books = Book_data.query.all()
    return render_template('book_list.html', form=form, books=books)

@myapp_obj.route('/modify_books/', methods=['GET', 'POST'])
@login_required
def modify_books():
    form = add_books_to_library()
    if form.validate_on_submit():
        book_info = Book_data(book_ttl=form.book_name.data, book_gere=form.book_genere.data, book_aval=form.book_available.data)
        db.session.add(book_info)
        db.session.commit()
        flash('Book added', 'success')
        return redirect(url_for('modify_books'))
    return render_template('add_book.html', form=form)

@myapp_obj.route('/books/', methods=['POST', 'GET'])
def books():
    books = Book_data.query.all()
    return render_template('browse.html', books=books)

@myapp_obj.route('/books_lib/', methods=['POST', 'GET'])
def books_lib():
    books = Book_data.query.all()
    return render_template('book_lib.html', books=books)

@myapp_obj.route('/admin_database', methods=['POST', 'GET'])
@login_required
def admin_database():
    login_info = User.query.all()
    books = Book_data.query.all()
    deletes = Delete_user.query.all()
    rent_books = Rent_books.query.all()
    return render_template('admin_database.html', login_info=login_info, books=books, deletes=deletes, rent_books=rent_books)
