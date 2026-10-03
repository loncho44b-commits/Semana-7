# Quantum Wallet: base de datos con SQLite

En esta actividad pasé las clases que hicimos en la semana anterior (`Usuario`, `UsuarioEmpresa` y `Wallet`) a una base de datos, para que la información no se pierda cuando el programa se cierra. Usé SQLite, que viene incluido con Python a través del módulo `sqlite3`, así que no hace falta instalar nada extra.

## Cómo pensé el diseño

Lo primero fue decidir qué merece tener una tabla propia. Terminé con dos:

- **usuarios**, donde vive la identidad de cada persona o empresa.
- **wallets**, donde vive el dinero.

Separé estas dos cosas porque son responsabilidades distintas: un usuario es quien es, y una wallet es lo que tiene. Así, si algún día un usuario necesita más de una wallet, no hay que rehacer la tabla de usuarios.

### Tabla `usuarios`

| Campo | Tipo | Para qué sirve |
|---|---|---|
| id_usuario | INTEGER, llave primaria | Número automático que identifica a cada usuario y nunca se repite |
| nombre | TEXT, obligatorio | Nombre del usuario |
| email | TEXT, único y obligatorio | Correo; no puede haber dos usuarios con el mismo |
| nit | TEXT | Identificación tributaria. Es opcional porque solo la necesitan los usuarios de empresa (`UsuarioEmpresa`) |

El `nit` me permite guardar tanto usuarios normales como de empresa en la misma tabla: si el campo viene vacío es un usuario común, y si trae un valor es una empresa.

### Tabla `wallets`

| Campo | Tipo | Para qué sirve |
|---|---|---|
| id_wallet | INTEGER, llave primaria | Número automático que identifica cada wallet |
| saldo | REAL, por defecto 0.0 | El dinero disponible; usa REAL para permitir centavos (por ejemplo 100.50) |
| id_propietario | INTEGER, llave foránea | Indica de qué usuario es la wallet |

### La relación entre las tablas

Para que el sistema sepa de quién es cada wallet, la columna `id_propietario` de `wallets` es una **llave foránea** que apunta a `id_usuario` de la tabla `usuarios`. Es decir, cada wallet pertenece a un usuario, y la base de datos no deja crear una wallet para un usuario que no existe.

Para que SQLite haga esa validación hay que activarla en cada conexión con `PRAGMA foreign_keys = ON;`, porque por defecto viene apagada. Por eso aparece al inicio de los dos scripts.

## Archivos del repositorio

- `configurar_db.py`: crea el archivo `quantum_wallet.db` y las dos tablas. Usa `CREATE TABLE IF NOT EXISTS`, así que se puede ejecutar varias veces sin que falle ni borre nada.
- `probar_insercion.py`: inserta un usuario y su wallet para comprobar que todo funciona, y luego muestra lo guardado con un `JOIN` entre las dos tablas. Tiene un `try/except` para avisar si el email ya existe, ya que es único.
- `quantum_wallet.db`: la base de datos ya creada y con los datos de prueba.

## Cómo ejecutarlo

Desde la terminal, dentro de la carpeta del proyecto y en este orden:

```
python configurar_db.py
python probar_insercion.py
```

El orden importa: el segundo script necesita que las tablas ya existan. Si se ejecuta `probar_insercion.py` otra vez, mostrará el mensaje de que el usuario ya existe, y eso es lo esperado porque el email no se puede repetir.

## Cómo comprobar que funcionó

Se puede abrir `quantum_wallet.db` con la extensión SQLite DB Viewer de VS Code, con DB Browser for SQLite o en el navegador con https://inloop.github.io/sqlite-viewer/. En la tabla `usuarios` aparece el usuario insertado, y en `wallets` su saldo con el `id_propietario` que lo enlaza a ese usuario.

## Algo que aprendí

Las bases de datos son mucho más estrictas que Python con los tipos de datos y las reglas: si un campo es obligatorio, único o apunta a otra tabla, la base lo hace cumplir por mí. Eso hace que los datos sean más confiables que si solo estuvieran en variables dentro del programa.
