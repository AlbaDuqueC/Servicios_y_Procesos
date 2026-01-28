import multiprocessing
import random
import time
import os

# Proceso 1: Escritura de 6 notas con decimales en un archivo
def generar_notas(nombre_archivo):
    # Variable de retorno con el nombre del archivo
    archivo_final = nombre_archivo
    # Creación de lista con 6 valores flotantes aleatorios
    lista_notas = [round(random.uniform(1, 10), 2) for _ in range(6)]
    # Apertura del fichero en modo escritura
    with open(nombre_archivo, 'w') as f:
        # Bucle para escribir cada nota en líneas separadas
        for nota in lista_notas:
            f.write(str(nota) + "\n")
    # Retorno del nombre del archivo procesado
    return archivo_final

# Proceso 2: Cálculo de media y registro en archivo común
def calcular_media(pack_datos):
    # Desglose de la ruta y el nombre del estudiante
    ruta, nombre_estudiante = pack_datos
    # Variable para almacenar el promedio calculado
    valor_promedio = 0.0
    # Lectura del archivo de notas individual
    with open(ruta, 'r') as f:
        # Conversión de líneas de texto a números decimales
        notas_float = [float(linea.strip()) for linea in f]
    # División de la suma total entre la cantidad de elementos
    valor_promedio = sum(notas_float) / len(notas_float)
    # Apertura del archivo de medias para añadir datos
    with open("medias.txt", "a") as f:
        # Almacenamiento del promedio y el nombre
        f.write(str(valor_promedio) + " " + str(nombre_estudiante) + "\n")
    # Retorno del valor de la media calculada
    return valor_promedio

# Proceso 3: Localización del valor máximo en el listado general
def obtener_nota_maxima():
    # Variable de texto para el reporte final
    reporte_final = "Error"
    # Inicialización de comparadores de máximo
    nota_top = -1.0
    nombre_top = ""
    # Lectura del archivo acumulado de medias
    with open("medias.txt", 'r') as f:
        # Recorrido de cada línea del fichero
        for linea in f:
            # División de la línea en componentes
            datos_linea = linea.split()
            # Comparación con la nota máxima actual
            if float(datos_linea[0]) > nota_top:
                # Actualización de la nota y el nombre ganadores
                nota_top = float(datos_linea[0])
                nombre_top = datos_linea[1]
    # Composición de la cadena informativa final
    reporte_final = "Máxima: " + str(nota_top) + " - Alumno: " + str(nombre_top)
    # Visualización del resultado por pantalla
    print(reporte_final)
    # Retorno del reporte completo
    return reporte_final

if __name__ == "__main__":
    # Eliminación de restos de ejecuciones pasadas
    if os.path.exists("medias.txt"): os.remove("medias.txt")
    # Marca de tiempo inicial
    t_inicio = time.time()
    # Generación de nombres para los 10 archivos de alumnos
    nombres_archivos = ["Alumno" + str(i) + ".txt" for i in range(1, 11)]
    # Gestión de 10 procesos simultáneos mediante Pool
    with multiprocessing.Pool(10) as grupo_procesos:
        # Lanzamiento paralelo de la generación de notas
        grupo_procesos.map(generar_notas, nombres_archivos)
        # Preparación de tuplas con datos para el cálculo de medias
        lista_argumentos = [(nombres_archivos[i], "Alumno" + str(i+1)) for i in range(10)]
        # Ejecución paralela de los promedios
        grupo_procesos.map(calcular_media, lista_argumentos)
    # Ejecución del proceso final tras las etapas previas
    obtener_nota_maxima()
    # Muestra del tiempo total de trabajo
    print("Tiempo: " + str(time.time() - t_inicio) + " s")