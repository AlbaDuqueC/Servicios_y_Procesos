import multiprocessing
import random
import time

# Proceso 1: Creación de 10 direcciones IP aleatorias
def proceso_1(cola_1_2):
    # Variable informativa del fin de la tarea
    estado_final = "Generación exitosa"
    # Bucle limitado a 10 iteraciones
    for _ in range(10):
        # Composición de la IP con números al azar
        ip = str(random.randint(1, 254)) + "." + str(random.randint(0, 255)) + "." + \
             str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
        # Envío de la IP hacia el siguiente eslabón
        cola_1_2.put(ip)
    # Colocación de marca de cierre en la cola
    cola_1_2.put("TERMINAR")
    # Salida de la función con el estado
    return estado_final

# Proceso 2: Selección de IPs pertenecientes a clases A, B o C
def proceso_2(cola_1_2, cola_2_3):
    # Variable para el mensaje de retorno
    resultado_filtro = "Filtrado completado"
    # Obtención del primer dato de la cola de entrada
    dato_ip = cola_1_2.get()
    # Procesamiento continuo mientras el dato sea distinto a la marca de cierre
    while dato_ip != "TERMINAR":
        # Conversión del primer fragmento de la IP a entero
        primer_bloque = int(dato_ip.split('.')[0])
        # Validación del rango correspondiente a clases A, B y C
        if 1 <= primer_bloque <= 223:
            # Transferencia de la IP válida al tercer proceso
            cola_2_3.put(dato_ip)
        # Petición del siguiente dato de la cola
        dato_ip = cola_1_2.get()
    # Propagación de la marca de cierre a la siguiente cola
    cola_2_3.put("TERMINAR")
    # Retorno de la variable descriptiva
    return resultado_filtro

# Proceso 3: Visualización de IPs y su clase de red
def proceso_3(cola_2_3):
    # Variable de estado para la salida de datos
    confirmacion = "Impresión finalizada"
    # Lectura del dato inicial filtrado
    dato_ip = cola_2_3.get()
    # Bucle de ejecución dependiente de la marca de cierre
    while dato_ip != "TERMINAR":
        # Extracción del primer octeto
        primer_num = int(dato_ip.split('.')[0])
        # Elección de la letra de clase según el valor numérico
        letra_clase = "A" if primer_num <= 127 else "B" if primer_num <= 191 else "C"
        # Muestra de la información formateada en consola
        print("IP: " + str(dato_ip) + " | Clase: " + str(letra_clase))
        # Lectura de la siguiente IP de la cola
        dato_ip = cola_2_3.get()
    # Devolución de la variable de confirmación
    return confirmacion

if __name__ == "__main__":
    # Instanciación de colas para la comunicación interprocesos
    vía_1 = multiprocessing.Queue()
    vía_2 = multiprocessing.Queue()
    # Inicio del cronómetro de ejecución
    comienzo = time.time()
    # Configuración de los procesos enlazados
    p1 = multiprocessing.Process(target=proceso_1, args=(vía_1,))
    p2 = multiprocessing.Process(target=proceso_2, args=(vía_1, vía_2))
    p3 = multiprocessing.Process(target=proceso_3, args=(vía_2,))
    # Arranque de los procesos en el orden lógico
    p1.start()
    p2.start()
    p3.start()
    # Bloqueo del programa hasta terminar las tareas
    p1.join()
    p2.join()
    p3.join()
    # Impresión del tiempo total transcurrido
    print("Tiempo total: " + str(time.time() - comienzo) + " segundos")