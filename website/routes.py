from datetime import datetime
from website.settings.roles import User, delete_roles, checkout_books_role, data_book
from website.settings.forms import login_page, sign_up, delete_user_page, checkout_book_page, add_books_form
from website import myapp_obj, db
from flask_login import login_user, logout_user, login_required, current_user
from flask import flash, render_template, redirect



#sets up the database
@myapp_obj.before_request
def create_db():
    db.create_all()

#this routes the log out, which it will send it back to home
@myapp_obj.route('/logout/')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/')

#This routes the login page, which we are able to check if it is an admin, librarian, or general user
@myapp_obj.route('/login/', methods=['GET', 'POST'])
def login():
    logout_user()
    form = login_page()
    if form.validate_on_submit():
        if form.submit.data:
            user_login = User.query.filter_by(username=form.username.data).first()
            if user_login and user_login.check_password(form.password.data):
                login_user(user_login)
                if user_login.role == 'admin':
                    return redirect('/home_admin/')
                elif user_login.role == 'librarian':
                    return redirect('/home_librarian/')
                elif user_login.role == 'student/general':
                    return redirect('/general_home/')
            else:
                flash("Username or Password is incorrect.")
    return render_template('login.html', form=form)
@myapp_obj.route('/checkout/', methods=['GET', 'POST'])
@login_required
def checkout_book():
    form = checkout_book_page()
    if form.validate_on_submit():
        book_ttl = data_book.query.filter_by(book_title=form.book_checkout.data).first()
        if book_ttl is None:
            flash("Book not found.")
        else:
            db.session.delete(book_ttl)
            db.session.commit()
            flash("Book checked out.")
            return redirect('/checkout/')
    books = data_book.query.all()
    return render_template('checkout_books_page.html', form=form, books=books)

#this gives the routing for the browse page, which we query the books
@myapp_obj.route('/browse/', methods=['POST', 'GET'])
def browse():
    books = data_book.query.all()
    return render_template('browse.html', user=current_user, books=books)

#Gives the routing for the admins and their pages
@myapp_obj.route('/home_admin/', methods=['POST', 'GET'])
@login_required
def home_admin():
    return render_template('admin_page.html', user=current_user)

#This routes to the admin database, which we can see the user logins, the books, and the deleted users.
@myapp_obj.route('/admin_database/', methods=['POST', 'GET'])
@login_required
def admin_database():
    login_info = User.query.all()
    books = data_book.query.all()
    delete = delete_roles.query.all()
    return render_template('database.html', login_info=login_info, books=books, deletes=delete)

#This routes to the delete page, where we are going to check for the user, then we are going to delete them
@myapp_obj.route('/delete/', methods=['POST', 'GET'])
@login_required
def delete_user():
    form = delete_user_page()
    if form.validate_on_submit():
        deleted_user = User.query.filter_by(username=form.deleted_username.data).first()
        if deleted_user:
            #this will delete the roles, according to the admin, which it will set their id and username when they delete the role
            user_ToBeDeleted = delete_roles(admin_username=current_user.username,  admin_id=current_user.id, deleted_user=deleted_user.username, user_id=deleted_user.id)
            #this will add in the deleted user into another database
            db.session.add(user_ToBeDeleted)
            #this will delete the user from the initial database
            db.session.delete(deleted_user)
            db.session.commit()
            flash("User deleted.")
        else:
            flash("Username does not exist.")
    return render_template('delete_user_page.html', form=form)

#Gives the routing for the librarians and their commands
@myapp_obj.route('/home_librarian/', methods=['POST', 'GET'])
@login_required
def home_librarian():
    return render_template('librarian_page.html', user=current_user)

#this gives the librarian view of the database
@myapp_obj.route('/library_books/', methods=['POST', 'GET'])
def library_books():
    books = data_book.query.all()
    return render_template('librarian_view.html', books=books)

#this adds in tn the books, which we are looking for the book name and genre
@myapp_obj.route('/add_books/', methods=['GET', 'POST'])
@login_required
def add_books_route():
    form = add_books_form()
    if form.validate_on_submit():
        book = data_book(book_title=form.book_name_add.data, book_genre=form.book_genre_add.data)
        db.session.add(book)
        db.session.commit()
        flash('Book added', 'success')
    return render_template('add_book.html', form=form)

#this gives the overall routing for when we register
@myapp_obj.route('/register/', methods=['POST', 'GET'])
def register():
    #initially we want to log out the user, every register
    logout_user()
    form = sign_up()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash("Username already exists.")
        else:
            user = User(username=form.username.data, password=form.password.data, role=form.role.data)
            #this will set the password of the user
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            #this will check with the login manager, which type of role they chose
            login_user(user)
            if user.role == 'admin':
                return redirect('/home_admin/')
            elif user.role == 'student/general':
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

#creates the routing to the home page
@myapp_obj.route("/")
def home_page():
    return render_template('home_page.html')