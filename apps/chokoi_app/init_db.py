from sqlalchemy import text

from modules.database import engine

with engine.connect() as conn:

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS productores (

        id SERIAL PRIMARY KEY,

        nombre TEXT,
        ubicacion TEXT,

        celular TEXT,
        redes TEXT,

        email TEXT,

        edit_token TEXT,

        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );

    """))

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS productos (

        id SERIAL PRIMARY KEY,

        productor_id INTEGER,

        producto TEXT,
        precio FLOAT,
        unidad TEXT

    );

    """))

    conn.commit()

print("Base de datos inicializada")
