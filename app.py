from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from conexiones import get_admin_connection, get_user_connection

app = Flask(__name__)
app.secret_key = "password"


# --- LOGIN, LOGOUT, INICIO ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        contraseña_hasheada = hashlib.md5(contraseña.encode()).hexdigest()

        cnx = get_user_connection()
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT correo, contraseña, es_administrador FROM login WHERE correo = %s"
        cursor.execute(query, (correo,))
        usuario = cursor.fetchone()

        cursor.close()
        cnx.close()

        if not usuario:
            return render_template("login.html", error="El correo no está registrado.")
        else:
            if usuario["contraseña"] == contraseña_hasheada:
                session["usuario"] = {
                    "correo": usuario["correo"],
                    "es_admin": usuario["es_administrador"] == 1,
                }
                return redirect(url_for("inicio"))
            else:
                return render_template("login.html", error="Contraseña incorrecta.")

    return render_template("login.html")


@app.route("/", methods=["GET"])
def inicio():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("inicio.html", usuario=session["usuario"])


@app.route("/recuperar", methods=["GET", "POST"])
def recuperar_contraseña():
    if request.method == "POST":
        correo = request.form["correo"].strip()

        conn = get_user_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT correo FROM Login WHERE correo = %s", (correo,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session["correo_para_recuperar"] = correo
            return redirect(url_for("cambiar_contraseña"))
        else:
            return render_template(
                "recuperar_contraseña.html", error="El correo no está registrado."
            )

    return render_template("recuperar_contraseña.html")


@app.route("/cambiar_contraseña", methods=["GET", "POST"])
def cambiar_contraseña():
    if "correo_para_recuperar" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nueva = request.form["nueva"]
        repetir = request.form["repetir"]

        if nueva != repetir:
            return render_template(
                "cambiar_contraseña.html", error="Las contraseñas no coinciden."
            )

        correo = session.pop("correo_para_recuperar")
        nueva_hasheada = hashlib.md5(nueva.encode()).hexdigest()

        conn = get_admin_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Login SET contraseña = %s WHERE correo = %s",
            (nueva_hasheada, correo),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("cambiar_contraseña.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# --- USUARIOS ---


@app.route("/usuarios", methods=["GET"])
def mostrar_usuarios():
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("inicio"))

    conn = get_admin_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT correo, es_administrador FROM Login")
    usuarios = cursor.fetchall()
    conn.close()

    return render_template(
        "usuarios/usuarios.html", usuario=session["usuario"], usuarios=usuarios
    )


@app.route("/usuarios/nuevo", methods=["GET"])
def nuevo_usuario():
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_usuarios"))

    return render_template("usuarios/nuevoUsuario.html", usuario=session["usuario"])


@app.route("/usuarios/crear", methods=["POST"])
def crear_usuario():
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_usuarios"))

    correo = request.form.get("correo", "").strip()
    contraseña = request.form.get("contraseña", "").strip()

    contraseña_hasheada = hashlib.md5(contraseña.encode()).hexdigest()

    es_admin = request.form.get("es_admin") == "on"

    if not correo or not contraseña:
        return render_template(
            "usuarios/nuevoUsuario.html",
            error="Correo y contraseña son obligatorios",
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Login (correo, contraseña, es_administrador)
        VALUES (%s, %s, %s)
    """,
        (correo, contraseña_hasheada, es_admin),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_usuarios"))


@app.route("/usuarios/editar/<string:correo>", methods=["POST"])
def editar_usuario(correo):
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_usuarios"))

    es_admin = request.form.get("es_admin") == "on"

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Login
        SET es_administrador = %s
        WHERE correo = %s
    """,
        (es_admin, correo),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_usuarios"))


@app.route("/usuarios/eliminar/<string:correo>", methods=["POST"])
def eliminar_usuario(correo):
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_usuarios"))

    if correo == session["usuario"]["correo"]:
        return redirect(url_for("mostrar_usuarios"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Login WHERE correo = %s", (correo,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_usuarios"))


# --- CLIENTES ---


@app.route("/clientes", methods=["GET"])
def mostrar_clientes():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()

    return render_template(
        "clientes/clientes.html", usuario=session["usuario"], clientes=clientes
    )


@app.route("/clientes/nuevo", methods=["GET"])
def nuevo_cliente():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("clientes/nuevoCliente.html", usuario=session["usuario"])


@app.route("/clientes/crear", methods=["POST"])
def crear_cliente():
    if "usuario" not in session:
        return redirect(url_for("login"))

    nombre = request.form.get("nombre", "").strip()
    direccion = request.form.get("direccion", "").strip()
    telefono = request.form.get("telefono", "").strip()
    correo = request.form.get("correo", "").strip()

    if not (nombre and direccion and telefono and correo):
        return render_template(
            "clientes/nuevoCliente.html",
            error="Todos los campos son obligatorios",
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Clientes (nombre, direccion, telefono, correo)
        VALUES (%s, %s, %s, %s)
    """,
        (nombre, direccion, telefono, correo),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_clientes"))


@app.route("/clientes/editar/<int:id_cliente>", methods=["POST"])
def editar_cliente(id_cliente):
    if "usuario" not in session:
        return redirect(url_for("login"))

    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Clientes
        SET nombre = %s, direccion = %s, telefono = %s, correo = %s
        WHERE id_cliente = %s
    """,
        (nombre, direccion, telefono, correo, id_cliente),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_clientes"))


@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar_cliente(id_cliente):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE id_cliente = %s", (id_cliente,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_clientes"))


# --- INSUMOS ---


@app.route("/insumos", methods=["GET"])
def mostrar_insumos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT i.*, p.nombre AS nombre_proveedor
        FROM Insumos i
        JOIN Proveedores p ON i.id_proveedor = p.id_proveedor
    """
    )
    insumos = cursor.fetchall()

    cursor.execute("SELECT id_proveedor, nombre FROM Proveedores")
    proveedores = cursor.fetchall()
    conn.close()

    return render_template(
        "insumos/insumos.html",
        usuario=session["usuario"],
        insumos=insumos,
        proveedores=proveedores,
    )


@app.route("/insumos/nuevo", methods=["GET"])
def nuevo_insumo():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_proveedor, nombre FROM Proveedores")
    proveedores = cursor.fetchall()
    conn.close()

    return render_template(
        "insumos/nuevoInsumo.html", proveedores=proveedores, usuario=session["usuario"]
    )


@app.route("/insumos/crear", methods=["POST"])
def crear_insumo():
    if "usuario" not in session:
        return redirect(url_for("login"))

    descripcion = request.form.get("descripcion", "").strip()
    tipo = request.form.get("tipo", "").strip()
    precio_unitario = request.form.get("precio_unitario", "").strip()
    id_proveedor = request.form.get("id_proveedor")

    if not (descripcion and tipo and precio_unitario and id_proveedor):
        error = "Todos los campos son obligatorios."
        conn = get_user_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_proveedor, nombre FROM Proveedores")
        proveedores = cursor.fetchall()
        conn.close()

        return render_template(
            "insumos/nuevoInsumo.html",
            error=error,
            proveedores=proveedores,
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Insumos (descripcion, tipo, precio_unitario, id_proveedor)
        VALUES (%s, %s, %s, %s)
    """,
        (descripcion, tipo, precio_unitario, id_proveedor),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_insumos"))


@app.route("/insumos/editar/<int:id_insumo>", methods=["POST"])
def editar_insumo(id_insumo):
    if "usuario" not in session:
        return redirect(url_for("login"))

    descripcion = request.form["descripcion"]
    tipo = request.form["tipo"]
    precio_unitario = request.form["precio_unitario"]
    id_proveedor = request.form["id_proveedor"]

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Insumos
        SET descripcion = %s, tipo = %s, precio_unitario = %s, id_proveedor = %s
        WHERE id_insumo = %s
    """,
        (descripcion, tipo, precio_unitario, id_proveedor, id_insumo),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_insumos"))


@app.route("/insumos/eliminar/<int:id_insumo>", methods=["POST"])
def eliminar_insumo(id_insumo):
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Insumos WHERE id_insumo = %s", (id_insumo,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_insumos"))


# --- PROVEEDORES ---


@app.route("/proveedores", methods=["GET"])
def mostrar_proveedores():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    conn.close()

    es_admin = session["usuario"].get("es_admin", False)

    return render_template(
        "proveedores/proveedores.html",
        usuario=session["usuario"],
        proveedores=proveedores,
        es_admin=es_admin,
    )


@app.route("/proveedores/nuevo", methods=["GET"])
def nuevo_proveedor():
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_proveedores"))

    return render_template(
        "proveedores/nuevoProveedor.html", usuario=session["usuario"]
    )


@app.route("/proveedores/crear", methods=["POST"])
def crear_proveedor():
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_proveedores"))

    nombre = request.form.get("nombre", "").strip()
    contacto = request.form.get("contacto", "").strip()

    if not (nombre and contacto):
        return render_template(
            "proveedores/nuevoProveedor.html",
            error="Todos los campos son obligatorios",
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Proveedores (nombre, contacto)
        VALUES (%s, %s)
    """,
        (nombre, contacto),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_proveedores"))


@app.route("/proveedores/editar/<int:id_proveedor>", methods=["POST"])
def editar_proveedor(id_proveedor):
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_proveedores"))

    nombre = request.form["nombre"]
    contacto = request.form["contacto"]

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Proveedores
        SET nombre = %s, contacto = %s 
        WHERE id_proveedor = %s
    """,
        (nombre, contacto, id_proveedor),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_proveedores"))


@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
def eliminar_proveedor(id_proveedor):
    if "usuario" not in session or not session["usuario"].get("es_admin"):
        return redirect(url_for("mostrar_proveedores"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Proveedores WHERE id_proveedor = %s", (id_proveedor,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_proveedores"))


# --- MÁQUINAS ---


@app.route("/maquinas", methods=["GET"])
def mostrar_maquinas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.*, c.nombre AS nombre_cliente
        FROM Maquinas m
        JOIN Clientes c ON m.id_cliente = c.id_cliente
    """
    )
    maquinas = cursor.fetchall()

    cursor.execute("SELECT id_cliente, nombre FROM Clientes")
    clientes = cursor.fetchall()

    conn.close()

    es_admin = session["usuario"].get("es_admin", False)

    return render_template(
        "maquinas/maquinas.html",
        usuario=session["usuario"],
        maquinas=maquinas,
        clientes=clientes,
        es_admin=es_admin,
    )


@app.route("/maquinas/nuevo", methods=["GET"])
def nueva_maquina():
    if "usuario" not in session:
        return redirect(url_for("login"))
    if not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_maquinas"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()

    return render_template(
        "maquinas/nuevaMaquina.html", usuario=session["usuario"], clientes=clientes
    )


@app.route("/maquinas/crear", methods=["POST"])
def crear_maquina():
    if "usuario" not in session:
        return redirect(url_for("login"))
    if not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_maquinas"))

    modelo = request.form.get("modelo", "").strip()
    id_cliente = request.form.get("id_cliente")
    ubicacion_cliente = request.form.get("ubicacion_cliente", "").strip()
    costo_alquiler_mensual = request.form.get("costo_alquiler_mensual", "").strip()

    if not (modelo and id_cliente and ubicacion_cliente and costo_alquiler_mensual):
        error = "Todos los campos son obligatorios."
        conn = get_user_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_cliente, nombre FROM Clientes")
        clientes = cursor.fetchall()
        conn.close()
        return render_template(
            "maquinas/nuevaMaquina.html",
            error=error,
            clientes=clientes,
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual)
        VALUES (%s, %s, %s, %s)
    """,
        (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_maquinas"))


@app.route("/maquinas/editar/<int:id_maquina>", methods=["POST"])
def editar_maquina(id_maquina):
    if "usuario" not in session:
        return redirect(url_for("login"))
    if not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_maquinas"))

    modelo = request.form["modelo"]
    id_cliente = request.form["id_cliente"]
    ubicacion_cliente = request.form["ubicacion_cliente"]
    costo_alquiler_mensual = request.form["costo_alquiler_mensual"]

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Maquinas
        SET modelo = %s, id_cliente = %s, ubicacion_cliente = %s, costo_alquiler_mensual = %s
        WHERE id_maquina = %s
    """,
        (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual, id_maquina),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_maquinas"))


@app.route("/maquinas/eliminar/<int:id_maquina>", methods=["POST"])
def eliminar_maquina(id_maquina):
    if "usuario" not in session:
        return redirect(url_for("login"))
    if not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_maquinas"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Maquinas WHERE id_maquina = %s", (id_maquina,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_maquinas"))


# --- TÉCNICOS ---


@app.route("/tecnicos", methods=["GET"])
def mostrar_tecnicos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Tecnicos")
    tecnicos = cursor.fetchall()
    conn.close()

    es_admin = session["usuario"].get("es_admin", False)

    return render_template(
        "tecnicos/tecnicos.html",
        usuario=session["usuario"],
        tecnicos=tecnicos,
        es_admin=es_admin,
    )


@app.route("/tecnicos/nuevo", methods=["GET"])
def nuevo_tecnico():
    if "usuario" not in session or not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_tecnicos"))

    return render_template("tecnicos/nuevoTecnico.html", usuario=session["usuario"])


@app.route("/tecnicos/crear", methods=["POST"])
def crear_tecnico():
    if "usuario" not in session or not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_tecnicos"))

    try:
        ci = int(request.form.get("ci"))
    except (ValueError, TypeError):
        return render_template(
            "tecnicos/nuevoTecnico.html",
            error="La CI debe ser un número entero.",
            usuario=session["usuario"],
        )

    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    telefono = request.form.get("telefono", "").strip()

    if not (ci and nombre and apellido and telefono):
        return render_template(
            "tecnicos/nuevoTecnico.html",
            error="Todos los campos son obligatorios.",
            usuario=session["usuario"],
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Tecnicos (ci, nombre, apellido, telefono)
        VALUES (%s, %s, %s, %s)
    """,
        (ci, nombre, apellido, telefono),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_tecnicos"))


@app.route("/tecnicos/editar/<int:ci>", methods=["POST"])
def editar_tecnico(ci):
    if "usuario" not in session or not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_tecnicos"))

    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Tecnicos
        SET nombre = %s, apellido = %s, telefono = %s
        WHERE ci = %s
    """,
        (nombre, apellido, telefono, ci),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_tecnicos"))


@app.route("/tecnicos/eliminar/<int:ci>", methods=["POST"])
def eliminar_tecnico(ci):
    if "usuario" not in session or not session["usuario"].get("es_admin", False):
        return redirect(url_for("mostrar_tecnicos"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tecnicos WHERE ci = %s", (ci,))
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_tecnicos"))


# --- REGISTRO DE CONSUMO ---


@app.route("/consumos", methods=["GET"])
def mostrar_consumos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT rc.id_consumo, m.modelo, i.descripcion, rc.fecha, rc.cantidad_usada
        FROM Registro_consumo rc
        JOIN Maquinas m ON rc.id_maquina = m.id_maquina
        JOIN Insumos i ON rc.id_insumo = i.id_insumo
        ORDER BY rc.fecha DESC
    """
    )
    consumos = cursor.fetchall()
    conn.close()

    return render_template(
        "consumos/consumos.html", usuario=session["usuario"], consumos=consumos
    )


@app.route("/consumos/nuevo", methods=["GET"])
def nuevo_consumo():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_maquina, modelo FROM Maquinas")
    maquinas = cursor.fetchall()

    cursor.execute("SELECT id_insumo, descripcion FROM Insumos")
    insumos = cursor.fetchall()

    conn.close()

    return render_template(
        "consumos/nuevoConsumo.html",
        usuario=session["usuario"],
        maquinas=maquinas,
        insumos=insumos,
    )


@app.route("/consumos/crear", methods=["POST"])
def crear_consumo():
    if "usuario" not in session:
        return redirect(url_for("login"))

    id_maquina = request.form.get("id_maquina")
    id_insumo = request.form.get("id_insumo")
    fecha = request.form.get("fecha")
    cantidad_usada = request.form.get("cantidad_usada")

    if not (id_maquina and id_insumo and fecha and cantidad_usada):
        return redirect(url_for("nuevo_consumo"))

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada)
        VALUES (%s, %s, %s, %s)
    """,
        (id_maquina, id_insumo, fecha, cantidad_usada),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_consumos"))


# --- REPORTES ---
@app.route("/reportes", methods=["GET"])
def reportes():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)

    # 1) Total mensual a cobrar a cada cliente (alquiler + consumo insumos)
    cursor.execute(
        """
                   SELECT c.nombre AS cliente,
                          SUM(m.costo_alquiler_mensual) AS total_alquiler,
                          COALESCE(SUM(rc.cantidad_usada * i.precio_unitario), 0) AS total_consumo,
                          SUM(m.costo_alquiler_mensual) +
                          COALESCE(SUM(rc.cantidad_usada * i.precio_unitario), 0) AS total_mes
                   FROM Clientes c
                            LEFT JOIN Maquinas m ON c.id_cliente = m.id_cliente
                            LEFT JOIN Registro_consumo rc ON m.id_maquina = rc.id_maquina
                            LEFT JOIN Insumos i ON rc.id_insumo = i.id_insumo
                   WHERE rc.fecha >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
                   GROUP BY c.id_cliente
                   """
    )
    totales_clientes = cursor.fetchall()

    # 2) Insumos con mayor consumo y costos (sumas y orden descendente)
    cursor.execute(
        """
                   SELECT i.descripcion,
                          SUM(rc.cantidad_usada) AS total_cantidad,
                          SUM(rc.cantidad_usada * i.precio_unitario) AS total_costo
                   FROM Insumos i
                            JOIN Registro_consumo rc ON i.id_insumo = rc.id_insumo
                   GROUP BY i.id_insumo
                   ORDER BY total_cantidad DESC LIMIT 10
                   """
    )
    insumos_mayor_consumo = cursor.fetchall()

    # 3) Técnicos con más mantenimientos realizados
    cursor.execute(
        """
                   SELECT t.nombre,
                          t.apellido,
                          COUNT(m.id_mantenimiento) AS cantidad_mantenimientos
                   FROM Tecnicos t
                            JOIN Mantenimientos m ON t.ci = m.ci_tecnico
                   GROUP BY t.ci
                   ORDER BY cantidad_mantenimientos DESC LIMIT 10
                   """
    )
    tecnicos_top = cursor.fetchall()

    # 4) Clientes con más máquinas instaladas
    cursor.execute(
        """
                   SELECT c.nombre,
                          COUNT(m.id_maquina) AS cantidad_maquinas
                   FROM Clientes c
                            JOIN Maquinas m ON c.id_cliente = m.id_cliente
                   GROUP BY c.id_cliente
                   ORDER BY cantidad_maquinas DESC LIMIT 10
                   """
    )
    clientes_top_maquinas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "reportes/reportes.html",
        totales_clientes=totales_clientes,
        insumos_mayor_consumo=insumos_mayor_consumo,
        tecnicos_top=tecnicos_top,
        clientes_top_maquinas=clientes_top_maquinas,
        usuario=session["usuario"],
    )


# --- MANTENIMIENTOS ---


@app.route("/mantenimientos", methods=["GET"])
def mostrar_mantenimientos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.*, ma.modelo AS modelo_maquina, t.nombre AS nombre_tecnico, t.apellido AS apellido_tecnico
        FROM Mantenimientos m
        JOIN Maquinas ma ON m.id_maquina = ma.id_maquina
        JOIN Tecnicos t ON m.ci_tecnico = t.ci
        ORDER BY m.fecha DESC
    """
    )
    mantenimientos = cursor.fetchall()
    conn.close()

    return render_template(
        "mantenimientos/mantenimientos.html",
        usuario=session["usuario"],
        mantenimientos=mantenimientos,
    )


@app.route("/mantenimientos/nuevo", methods=["GET"])
def nuevo_mantenimiento():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conn = get_user_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_maquina, modelo FROM Maquinas")
    maquinas = cursor.fetchall()
    cursor.execute("SELECT ci, nombre, apellido FROM Tecnicos")
    tecnicos = cursor.fetchall()
    conn.close()

    return render_template(
        "mantenimientos/nuevoMantenimiento.html",
        usuario=session["usuario"],
        maquinas=maquinas,
        tecnicos=tecnicos,
    )


@app.route("/mantenimientos/crear", methods=["POST"])
def crear_mantenimiento():
    if "usuario" not in session:
        return redirect(url_for("login"))

    id_maquina = request.form.get("id_maquina")
    ci_tecnico = request.form.get("ci_tecnico")
    tipo = request.form.get("tipo").strip()
    fecha = request.form.get("fecha")
    observaciones = request.form.get("observaciones", "").strip()

    if not (id_maquina and ci_tecnico and tipo and fecha):
        error = "Todos los campos excepto observaciones son obligatorios."
        conn = get_user_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_maquina, modelo FROM Maquinas")
        maquinas = cursor.fetchall()
        cursor.execute("SELECT ci, nombre, apellido FROM Tecnicos")
        tecnicos = cursor.fetchall()
        conn.close()

        return render_template(
            "mantenimientos/nuevoMantenimiento.html",
            error=error,
            usuario=session["usuario"],
            maquinas=maquinas,
            tecnicos=tecnicos,
        )

    conn = get_admin_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (id_maquina, ci_tecnico, tipo, fecha, observaciones),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("mostrar_mantenimientos"))


# --- INICIO APP ---
if __name__ == "__main__":
    app.run(debug=True)
