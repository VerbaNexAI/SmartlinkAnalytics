import os
from config.db import conn_db
from flask import Flask, render_template, redirect, request, url_for, session, flash
from config.db_queries import authenticate_user, check_email_exists, register_new_user

app = Flask(__name__)
app.secret_key = os.getenv('KEY')

@app.route("/", methods=['GET', 'POST'])
def login():
    """Route to display the login page and handle login.

    :returns: The login page or redirects to the menu if login is successful.
    :rtype: str or Response
    """
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = authenticate_user(email, password)

        if user:
            session["user"] = user
            return redirect(url_for("menu"))
        else:
            error = "Incorrect username or password."
            flash(error, 'error')

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Route to display the registration page and handle user registration.

    :returns: The menu page if registration is successful, otherwise redirects to the registration page.
    :rtype: str or Response
    """
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Input validation
        if not first_name or not last_name or not email or not password or not confirm_password:
            flash("All fields are required.", 'error')
        elif password != confirm_password:
            flash("Passwords do not match.", 'error')
        elif not email.endswith("@seringtec.com"):
            flash("Email must be from the @seringtec.com domain.", 'error')
        elif check_email_exists(email):
            flash("Email is already registered.", 'error')
        else:
            if register_new_user(first_name, last_name, email, password):
                session["user"] = {"first_name": first_name, "last_name": last_name}
                return redirect(url_for("menu"))
            else:
                flash("Error registering user.", 'error')

    return render_template("login.html")

@app.route('/menu')
def menu():
    """Route to display the main menu page.

    :returns: The menu page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('menu.html', first_name=first_name, last_name=last_name)

@app.route('/spid')
def spid():
    """Route to display the SPID page.

    :returns: The SPID page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('index.html', first_name=first_name, last_name=last_name)

@app.route('/sel')
def sel():
    """Route to display the SEL page.

    :returns: The SEL page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('sel.html', first_name=first_name, last_name=last_name)

@app.route('/spi')
def spi():
    """Route to display the SPI page.

    :returns: The SPI page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('spi.html', first_name=first_name, last_name=last_name)

@app.route('/s3d')
def s3d():
    """Route to display the S3D page.

    :returns: The S3D page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('menu-s3d.html', first_name=first_name, last_name=last_name)

@app.route('/mecanica')
def mecanica():
    """Route to display the mecanica page.

    :returns: The mecanica page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('mecanica.html', first_name=first_name, last_name=last_name)

@app.route('/instrumentacion')
def instrumentacion():
    """Route to display the instrumentacion page.

    :returns: The instrumentacion page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('instrumentacion.html', first_name=first_name, last_name=last_name)

@app.route('/civil')
def civil():
    """Route to display the civil page.

    :returns: The civil page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('civil.html', first_name=first_name, last_name=last_name)

@app.route('/electrica')
def electrica():
    """Route to display the electrica page.

    :returns: The electrica page or redirects to the login page if the user is not logged in.
    :rtype: str or Response
    """
    if 'user' not in session:
        return redirect(url_for('login'))

    session_data = session['user']
    first_name = session_data['first_name']
    last_name = session_data['last_name']

    return render_template('electrica.html', first_name=first_name, last_name=last_name)

@app.route('/logout')
def logout():
    """Route to log out the user.

    :returns: Redirects to the login page.
    :rtype: Response
    """
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



