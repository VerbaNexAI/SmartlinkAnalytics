from flask import Flask, render_template, redirect, request, url_for, session, flash
import pyodbc
from config.db import conn_db


app = Flask(__name__, static_folder='static')
app.secret_key = 'tu_clave_secreta'  # Clave secreta para firmar las cookies de sesión

# Ruta para mostrar la página de inicio de sesión y manejar el inicio de sesión
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["password"]

        cur = conn_db().cursor()
        sql = f"SELECT * FROM Usuarios WHERE Correo=? AND Contraseña=?;"
        rows = cur.execute(sql, (email, contrasena)).fetchall()

        if len(rows) > 0:
            session["usuario"] = {"nombre": rows[0][0], "apellido": rows[0][1]}
            return redirect(url_for("menu"))
        else:
            error = "Usuario o Contraseña incorrectos."
            flash(error, 'error')  # Almacenar el mensaje de error como un mensaje flash

    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        email = request.form["correo"]
        contrasena = request.form["contraseña"]
        confirmar_contrasena = request.form["conf_contraseña"]

        print("Procesando formulario de registro...")

        # Validación de entradas
        if not nombre or not apellido or not email or not contrasena or not confirmar_contrasena:
            flash("Todos los campos son obligatorios.", 'error')
        elif contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden.", 'error')
        elif not email.endswith("@seringtec.com"):
            flash("El correo electrónico debe ser del dominio @seringtec.com.", 'error')
        else:
            try:
                conexion = conn_db()
                cur = conexion.cursor()
                sql_verificar = "SELECT * FROM Usuarios WHERE Correo=?;"
                rows = cur.execute(sql_verificar, (email,)).fetchall()

                if len(rows) > 0:
                    flash("El correo electrónico ya está registrado.", 'error')
                else:
                    sql_insertar = "INSERT INTO Usuarios (nombre, apellido, correo, contraseña) VALUES (?, ?, ?, ?);"
                    cur.execute(sql_insertar, (nombre, apellido, email, contrasena))
                    conexion.commit()
                    cur.close()
                    # Redirigir al usuario a otra página después de un registro exitoso
                    session["usuario"] = {"nombre": nombre, "apellido": apellido}
                    return redirect(url_for("menu"))
            except Exception as e:
                flash(f"Error al registrar usuario: {e}", 'error')

    print("Redireccionando al menú principal...")
    return redirect(url_for('menu'))



# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la sesión del usuario
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Ruta para el menú después de iniciar sesión
@app.route('/menu')
def menu():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Recuperar los datos de la sesión
    datos_sesion = session['usuario']
    nombre = datos_sesion['nombre']
    apellido = datos_sesion['apellido']

    # Renderizar la página del menú
    return render_template('index.html', nombre=nombre, apellido=apellido)

if __name__ == '__main__':
    app.run(debug=True)

    


