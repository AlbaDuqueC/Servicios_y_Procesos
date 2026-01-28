import multiprocessing
import time

# Proceso 1: Selección de títulos coincidentes con el año
def filtrar_peliculas(fichero_origen, año_filtro, cola_salida):
    # Variable de estado de la lectura
    estado_proceso = "Lectura finalizada"
    # Bloque de seguridad para lectura de archivos
    try:
        # Apertura del catálogo de películas
        with open(fichero_origen, 'r', encoding='utf-8') as f:
            # Iteración sobre cada línea del catálogo
            for linea in f:
                # División del nombre y el año mediante punto y coma
                celdas = linea.strip().split(';')
                # Validación de coincidencia con el año buscado
                if len(celdas) == 2 and celdas[1].strip() == str(año_filtro):
                    # Inserción del nombre de la película en la cola
                    cola_salida.put(celdas[0].strip())
    # Captura de posibles fallos de archivo o formato
    except Exception:
        estado_proceso = "Error en el fichero"
    # Envío de aviso de parada para el proceso receptor
    cola_salida.put("FIN_DATOS")
    # Devolución de la variable de estado
    return estado_proceso

# Proceso 2: Almacenamiento de títulos en un fichero específico
def guardar_resultados(año_clave, cola_entrada):
    # Construcción del nombre del archivo de salida
    nombre_fichero = "peliculas" + str(año_clave) + ".txt"
    # Recogida del primer elemento de la cola
    item = cola_entrada.get()
    # Apertura de un nuevo fichero de texto para escritura
    with open(nombre_fichero, 'w', encoding='utf-8') as f:
        # Ejecución del bucle mientras el dato no sea la marca de fin
        while item != "FIN_DATOS":
            # Escritura del nombre de la película recibida
            f.write(item + "\n")
            # Petición de un nuevo dato a la cola
            item = cola_entrada.get()
    # Retorno del nombre del fichero creado
    return nombre_fichero

if __name__ == "__main__":
    # Entrada de datos desde el teclado
    año_buscar = input("Año de estreno: ")
    ruta_fichero = input("Ruta del catálogo: ")
    # Creación de una cola para mover datos entre procesos
    vía_comunicacion = multiprocessing.Queue()
    # Registro de tiempo inicial
    instante_inicial = time.time()
    # Declaración de los procesos de lectura y escritura
    p_filtro = multiprocessing.Process(target=filtrar_peliculas, args=(ruta_fichero, año_buscar, vía_comunicacion))
    p_archivo = multiprocessing.Process(target=guardar_resultados, args=(año_buscar, vía_comunicacion))
    # Inicio de los procesos
    p_filtro.start()
    p_archivo.start()
    # Espera hasta completar la escritura
    p_filtro.join()
    p_archivo.join()
    # Finalización con reporte de tiempo
    print("Duración: " + str(time.time() - instante_inicial) + " s")