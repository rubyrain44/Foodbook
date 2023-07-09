from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask_app.models.user import User


#INDEX
@app.route('/')
def index():
    return render_template('index.html')

#LOGOUT
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    #Clears the session on logout
    return redirect ('/') 

#REGISTER PAGE
@app.route('/register')
def register():
    return render_template('register.html')

#REGISTER FORM
@app.route('/register', methods=['POST'])
def registerForm():
    if not User.validate_user(request.form):
        return redirect('/register')
        #Redirects the user back to the page if validations aren't met/passed 
    pw_hash = bcrypt.generate_password_hash(request.form['register_password'])
    #Hashes the registered password from the request.form
    print(pw_hash)
    data = {
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    #Complies the data from the request.form and the bcrypt hash and then proceeds to pass it into the user creation method below,
    # and attaching the created user to the user logged in in session, allowing them to stay logged in after redirect
    session['user_id'] = User.create_user(data)
    print(session['user_id'])
    return redirect ('/dashboard')


#LOGIN CURRENT USER FORM
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Invalid Email/Password")
        return redirect('/')
    #The user logs in with their email, and either meets the conditions, or is checked to see if their email is already registered.
    #If they meet the requirements met, then that user is set to the user logged in in session
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


#SUCCESSFUL REDIRECT TO DASHBOARD#
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        session_user = User.get_user({'id' : session['user_id']})
        #This step checks if a user is logged in and in session, and if so, they are attached to 'user', to allow data to be passed
        #to the page that is rendered.
        return render_template ('dashboard.html', session_user=session_user)
    return redirect ('/')



