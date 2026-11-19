from flask import Flask, render_template, request, redirect, url_for, flash
from database import obtener_conexion, crear_tabla

app = Flask(__name__)
app.secret_key = "clave-agenda-contactos"

crear_tabla()

# MOSTRAR CONTACTOS
@app.route("/")
def inicio():
    conexion = obtener_conexion()

    contactos = conexion.execute(
        "SELECT * FROM contactos ORDER BY nombre"
    ).fetchall()

    conexion.close()

    return render_template("index.html", contactos=contactos)

# AGREGAR CONTACTO
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    correo = request.form.get("correo", "").strip()
    categoria = request.form.get("categoria", "").strip()

    if not nombre or not telefono or not categoria:
        flash("Completa los campos obligatorios.")
        return redirect(url_for("inicio"))

    conexion = obtener_conexion()

    conexion.execute("""
        INSERT INTO contactos
        (nombre, telefono, correo, categoria)
        VALUES (?, ?, ?, ?)
    """, (nombre, telefono, correo, categoria))

    conexion.commit()
    conexion.close()

    flash("Contacto guardado correctamente.")
    return redirect(url_for("inicio"))

# EDITAR CONTACTO
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = obtener_conexion()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if not nombre or not telefono or not categoria:
            conexion.close()
            flash("Completa los campos obligatorios.")
            return redirect(url_for("editar", id=id))

        conexion.execute("""
            UPDATE contactos
            SET nombre = ?, telefono = ?, correo = ?, categoria = ?
            WHERE id = ?
        """, (nombre, telefono, correo, categoria, id))

        conexion.commit()
        conexion.close()

        flash("Contacto actualizado.")
        return redirect(url_for("inicio"))

    contacto = conexion.execute(
        "SELECT * FROM contactos WHERE id = ?", (id,)
    ).fetchone()

    conexion.close()

    if contacto is None:
        flash("El contacto no existe.")
        return redirect(url_for("inicio"))

    return render_template("editar.html", contacto=contacto)

# ELIMINAR CONTACTO
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = obtener_conexion()

    conexion.execute(
        "DELETE FROM contactos WHERE id = ?", (id,)
    )

    conexion.commit()
    conexion.close()

    flash("Contacto eliminado.")
    return redirect(url_for("inicio"))
print("iniciando agenda de contactos...")
if __name__ == "__main__":
    app.run(debug=True)
