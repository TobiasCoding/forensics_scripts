import sqlite3

terminos_de_busqueda_separados_por_comas = '''g'''
db_target = 'dbprueba.db'

def buscar_en_todas_las_tablas(db_file, termino_busqueda):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    resultados = []
    for tabla in tablas:
        tabla_nombre = tabla[0]
        cursor.execute(f"PRAGMA table_info({tabla_nombre})")
        columnas = cursor.fetchall()
        for columna in columnas:
            columna_nombre = columna[1]
            consulta = f"SELECT * FROM {tabla_nombre} WHERE {columna_nombre} LIKE ?"
            cursor.execute(consulta, ('%' + termino_busqueda + '%',))
            resultados_tabla = cursor.fetchall()
            for resultado in resultados_tabla:
                resultados.append((tabla_nombre,resultado))
    conn.close()
    return resultados

print("\n> Listado de términos de búsqueda: ",terminos_de_busqueda_separados_por_comas)
term_list = terminos_de_busqueda_separados_por_comas.split(',')
id_match = 0
for term in term_list:
    resultados = buscar_en_todas_las_tablas(db_target, term)
    if resultados:
        for tabla, resultado in resultados:
            if id_match == 0: print("> Se encontraron coincidencias:\nNRO.   |    TABLA     |   COINCIDENCIA\n_______|______________|____________________________")
            id_match +=1
            print(f"{id_match}      |   '{tabla}'   |   {resultado}")
    else: print('> No se encontraron coincidencias.')
print("> Fin de ejecución")
