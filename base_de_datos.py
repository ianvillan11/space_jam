import sqlite3

def crear_tabla_puntuaciones():
    with sqlite3.connect("puntajes") as conexion:
        try:
            sentencia = ''' 
            create table puntuaciones 
            (
                id integer primary key autoincrement,
                nombre text,
                puntuacion integer
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla de puntuaciones")
        except sqlite3.OperationalError:
            print("La tabla de puntuaciones, fue actualizada")
        except:
            print("Error al crear la tabla")
 
def leer_tabla_puntuaciones():
    with sqlite3.connect("puntajes") as conexion:

        cursor = conexion.execute("SELECT nombre, puntuacion from \
                puntuaciones ORDER BY puntuacion DESC LIMIT 10")
        resultados = cursor.fetchall()

    return resultados

def modificar_tabla_puntuaciones(nombre_ingresado,puntaje):
    with sqlite3.connect("puntajes") as conexion:

        try:
            conexion.execute("insert into puntuaciones (nombre, puntuacion)\
                values(?,?)",(nombre_ingresado, puntaje))
            conexion.commit()
        except:
            print("Error al insertar puntuacion")