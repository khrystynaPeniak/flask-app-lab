from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash 
from datetime import timedelta, datetime
from .forms import RegistrationForm, LoginForm
from .models import User
from .utils import delete_old_user_image, save_user_image
from flask_login import login_user, login_required, current_user, logout_user
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from .. import db  

@user_bp.route("/set-theme/<theme>")
def set_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'light'  
    
    response = make_response(redirect(url_for("users.get_profile")))
    response.set_cookie('theme_preference', theme, max_age=timedelta(days=365))  
    flash(f"Theme changed to {theme} mode", "success")
    return response

@user_bp.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if "username" not in session:
        flash("Error: access denied. Please login.", "danger")
        return redirect(url_for("users.login"))
    
    if request.method == "POST":
        response = make_response(redirect(url_for("users.get_profile")))
        
        if "add_cookie" in request.form:
            key, value = request.form.get("cookie_key"), request.form.get("cookie_value")
            if key and value:
                expiry = int(request.form.get("cookie_expiry", 3600))
                response.set_cookie(key, value, max_age=timedelta(seconds=expiry))
                flash(f"Cookie '{key}' added successfully.", "success")
            
        elif "delete_cookie_key" in request.form:
            key = request.form.get("delete_key")
            if key in request.cookies:
                response.set_cookie(key, "", expires=0)
                flash(f"Cookie '{key}' deleted.", "success")
                
        elif "delete_all_cookies" in request.form:
            for key in request.cookies:
                if key not in ['session', 'theme_preference']:  
                    response.set_cookie(key, "", expires=0)
            flash("All cookies deleted.", "success")
            
        return response
    
    theme = request.cookies.get('theme_preference', 'light')
    
    cookies = [(k, v) for k, v in request.cookies.items() 
               if k not in ['session', 'theme_preference']]
    
    return render_template("profile.html", username=session["username"], cookies=cookies, theme=theme
    )
    
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_password = User.hash_password(form.password.data)
        
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account for {form.username.data} was created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')
    
@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            #session["username"] = username
            login_user(user, remember=form.remember.data)
            flash('You logged in successfully!', 'success')
            return redirect(url_for('users.account'))
        flash("Error: Invalid username or password.", "danger")
    return render_template("login.html", form=form, title='Login')


@user_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)

@user_bp.route('/get-all-users', methods=['GET'])
@login_required
def get_all_users():
    users = User.query.all()
    users_count = len(users)
    return render_template('users_list.html', users=users, users_count=users_count)

@user_bp.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@user_bp.route('account/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    account = current_user
    form = UpdateAccountForm(obj=account)
    if form.validate_on_submit():
        account.username = form.username.data
        account.email = form.email.data
        account.about_me = form.about_me.data

        file = form.image_file.data
        if file and not isinstance(file, str):  
            delete_old_user_image(user_bp, account.image_file)
            new_filename = save_user_image(file, user_bp)
            account.image_file = new_filename

        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('users.account'))

    return render_template('edit_page.html', form=form)

@user_bp.route('account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            new_hashed_password = User.hash_password(form.new_password.data)
            current_user.password = new_hashed_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Current password is incorrect!', 'danger')
            
    return render_template('change_password.html', form=form)

@user_bp.route("/hi/<string:name>") 
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   
    #year = 2024 - age
    return render_template("hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)   
    print(to_url)
    return redirect(to_url)  

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', 'black', max_age=timedelta(seconds=60))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response