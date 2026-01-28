
from multiprocessing import Process, Queue
import time

"""Realiza el ejercicio anterior pero esta vez va a haber otra función que lea los números de un 
fichero. En el fichero habrá un número por línea. En este caso, tienes que llevar a cabo una 
comunicación entre los dos procesos utilizando colas (Queue), de forma que la función que se 
encarga de leer los números los guarde en la cola, y la función que realiza la suma, recibirá 
la cola y tomará de ahí los números. La función que lee el fichero, una vez haya terminado de 
leer y de añadir elementos a la cola, debe añadir un objeto None para que el receptor sepa cuándo 
terminar de leer de la cola."""

# Función que recibe números de la cola y los suma
def suma_numerines(numerin):
    suma = 0
    # Bucle infinito hasta recibir None
    while True:
        # Obtiene un número de la cola (espera si está vacía)
        n = numerin.get()
        # Si recibe None, termina el bucle
        if n is None:
            break
        # Acumula el número recibido
        suma += n
    # Imprime la suma total
    print("Suma total del fichero:", suma)

# Función que lee números del fichero y los mete en la cola
def leer_numerines_de_fichero_muy_chulo(q, ruta_fichero):
    # Abre el fichero en modo lectura texto
    with open(ruta_fichero, 'rt') as f:
        # Recorre cada línea del fichero
        for linea in f:
            # Elimina espacios en blanco al inicio y final
            linea = linea.strip()
            # Si la línea no está vacía
            if linea:
                # Convierte a entero y lo mete en la cola
                q.put(int(linea))
    # Mete None en la cola para indicar fin
    q.put(None)

# Protección para multiprocessing
if __name__ == "__main__":
    # Ruta del fichero con los números
    ficherin = 'Tema2\\Ejercicio3\\numerines.txt'
    # Crea una cola para comunicación entre procesos
    queue = Queue()
    # Marca tiempo de inicio
    start_time = time.time()
    # Crea proceso que lee el fichero y mete números en la cola
    p1 = Process(target=leer_numerines_de_fichero_muy_chulo, args=(queue, ficherin))
    # Crea proceso que lee de la cola y suma
    p2 = Process(target=suma_numerines, args=(queue,))
    # Inicia el proceso lector
    p1.start()
    # Inicia el proceso sumador
    p2.start()
    # Espera a que termine el proceso lector
    p1.join()
    # Espera a que termine el proceso sumador
    p2.join()
    # Marca tiempo de fin
    end_time = time.time()
    # Mensaje de finalización
    print("Finiquitao")
    # Calcula y muestra el tiempo transcurrido
    print(f"Tiempo: {end_time - start_time:.2f} segundos")