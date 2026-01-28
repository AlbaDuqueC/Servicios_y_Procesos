import multiprocessing
import time

# Función que acepta una vocal y devuelve su frecuencia en el archivo
def contar_vocal(vocal, ruta_fichero):
    # Inicialización de la variable para el resultado numérico
    conteo_total = 0
    # Apertura del archivo dentro de un bloque de control de errores
    try:
        # Lectura del fichero con codificación universal
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            # Transformación del texto a minúsculas para facilitar el conteo
            contenido = f.read().lower()
            # Cálculo de las repeticiones de la vocal específica
            conteo_total = contenido.count(vocal)
            # Muestra del dato parcial en la consola
            print("Vocal '" + str(vocal) + "': " + str(conteo_total))
    # Gestión del error si el archivo no existe en la ruta
    except FileNotFoundError:
        # Asignación de valor cero ante la ausencia del archivo
        conteo_total = 0
    # Retorno de la variable con el valor final obtenido
    return conteo_total

if __name__ == "__main__":
    # Definición del nombre del fichero de entrada
    archivo = "texto.txt"
    # Conjunto de vocales para procesar
    vocales = ['a', 'e', 'i', 'o', 'u']
    # Contenedor para los objetos de proceso
    procesos = []
    # Almacenamiento del instante de inicio
    inicio = time.time()
    
    # Ciclo para crear los 5 procesos paralelos
    for v in vocales:
        # Configuración de cada proceso con su tarea y argumentos
        p = multiprocessing.Process(target=contar_vocal, args=(v, archivo))
        # Inserción del proceso en la lista de gestión
        procesos.append(p)
        # Activación del proceso para ejecución paralela
        p.start()

    # Ciclo de espera para la finalización de tareas
    for p in procesos:
        # Sincronización del proceso con el programa principal
        p.join()
        
    # Impresión de la duración total del programa
    print("Tiempo total: " + str(time.time() - inicio) + " segundos")