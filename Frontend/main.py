from flask import Flask, render_template, redirect, request, url_for, session, flash
import pyodbc
from config.db import conn_db

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Secret key to sign session cookies

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

        cur = conn_db().cursor()
        sql = "SELECT * FROM Usuarios WHERE Correo=? AND Contraseña=?;"
        rows = cur.execute(sql, (email, password)).fetchall()

        if len(rows) > 0:
            session["user"] = {"first_name": rows[0][0], "last_name": rows[0][1]}
            return redirect(url_for("menu"))
        else:
            error = "Incorrect username or password."
            flash(error, 'error')  # Store the error message as a flash message

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
        else:
            try:
                connection = conn_db()
                cur = connection.cursor()
                sql_verify = "SELECT * FROM Usuarios WHERE Correo=?;"
                rows = cur.execute(sql_verify, (email,)).fetchall()

                if len(rows) > 0:
                    flash("Email is already registered.", 'error')
                else:
                    sql_insert = "INSERT INTO Usuarios (nombre, apellido, correo, contraseña) VALUES (?, ?, ?, ?);"
                    cur.execute(sql_insert, (first_name, last_name, email, password))
                    connection.commit()
                    cur.close()
                    # Redirect the user to another page after successful registration
                    session["user"] = {"first_name": first_name, "last_name": last_name}
                    return redirect(url_for("menu"))
            except Exception as e:
                flash(f"Error registering user: {e}", 'error')

    print("Redirecting to the main menu...")
    return redirect(url_for('menu'))

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

    return render_template('s3d.html', first_name=first_name, last_name=last_name)

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
