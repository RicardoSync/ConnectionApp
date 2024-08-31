import sqlite3

def agregar_columna_diaCorte():
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    
    # Verificar si la columna 'diaCorte' ya existe
    cursor.execute("PRAGMA table_info(clientes)")
    columnas = [col[1] for col in cursor.fetchall()]
    
    if 'diaCorte' not in columnas:
        # Agregar la nueva columna 'diaCorte'
        cursor.execute('''
            ALTER TABLE clientes
            ADD COLUMN diaCorte TEXT NOT NULL DEFAULT ''
        ''')
        print("Columna 'diaCorte' agregada con éxito.")
    else:
        print("La columna 'diaCorte' ya existe en la tabla.")
    
    conn.commit()
    conn.close()

# Llamar a la función para agregar la columna
agregar_columna_diaCorte()
