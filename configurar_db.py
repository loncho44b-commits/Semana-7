import sqlite3

# Se crea el archivo quantum_wallet.db
conexion = sqlite3.connect("quantum_wallet.db")

# El cursor es quien ejecuta las sentencias SQL
cursor = conexion.cursor()

# Activar el soporte de llaves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# Definimos la estructura de las tablas
script_tablas = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    nit TEXT
);

CREATE TABLE IF NOT EXISTS wallets (
    id_wallet INTEGER PRIMARY KEY AUTOINCREMENT,
    saldo REAL DEFAULT 0.0,
    id_propietario INTEGER NOT NULL,
    FOREIGN KEY (id_propietario) REFERENCES usuarios(id_usuario)
);
"""

# Ejecutamos el script
cursor.executescript(script_tablas)
print("Tablas creadas con éxito.")

# Guardar los cambios físicamente
conexion.commit()

# Cerrar la comunicación con la base de datos
conexion.close()
print("Conexión cerrada.")
