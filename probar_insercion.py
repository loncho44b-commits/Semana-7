import sqlite3

# Prueba rápida de inserción
conexion = sqlite3.connect("quantum_wallet.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

try:
    # 1. Insertar un usuario
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, nit) VALUES (?, ?, ?)",
        ("Jhon peñaranda", "loncho44b@gmail.com", "1004945539"),
    )
    # Recuperamos el id que la base de datos le asignó al usuario
    id_usuario = cursor.lastrowid

    # 2. Insertar su wallet, vinculada con la llave foránea
    cursor.execute(
        "INSERT INTO wallets (saldo, id_propietario) VALUES (?, ?)",
        (100.50, id_usuario),
    )

    conexion.commit()
    print("Usuario y wallet insertados correctamente.")
except sqlite3.IntegrityError:
    print("El usuario ya existe (el email es UNICO).")

# Verificación: mostrar lo que quedó guardado (JOIN entre las dos tablas)
cursor.execute("""
    SELECT u.id_usuario, u.nombre, u.email, u.nit, w.id_wallet, w.saldo
    FROM usuarios u
    JOIN wallets w ON w.id_propietario = u.id_usuario
""")
for fila in cursor.fetchall():
    print(fila)

conexion.close()
