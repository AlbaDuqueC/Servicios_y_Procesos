
from multiprocessing import Process, Queue, Pipe
import time

"""En este caso, vuelve a realizar la comunicación entre procesos pero usando tuberías (Pipe), 
de forma que la función que se encarga de leer los números del fichero se los envíe (send) al 
proceso que se encarga de la suma. El proceso que suma los números tiene que recibir (recv) un 
número y realizar la suma. Una vez que el proceso que lee el fichero termine de leer números en 
el fichero, debe enviar un None. El que recibe números dejará de realizar sumas cuando reciba 
un None."""

# Función que recibe números por el pipe y los suma
def suma_numerines(numerin):
    suma = 0
    # Bucle infinito hasta recibir None
    while True:
        # Recibe un número del pipe (espera si no hay datos)
        n = numerin.recv()
        # Si recibe None, termina el bucle
        if n is None:
            break
        # Acumula el número recibido
        suma += n
    # Imprime la suma total
    print("Suma total del fichero:", suma)

# Función que lee números del fichero y los envía por el pipe
def leer_numerines_de_fichero_muy_chulo(q, ruta_fichero):
    # Abre el fichero en modo lectura
    with open(ruta_fichero, 'r') as f:
        # Recorre cada línea del fichero
        for linea in f:
            # Elimina espacios en blanco
            linea = linea.strip()
            # Si la línea no está vacía
            if linea:
                # Envía el número convertido a entero por el pipe
                q.send(int(linea))
    # Envía None para indicar fin
    q.send(None)
    # Cierra la conexión del pipe
    q.close()

# Protección para multiprocessing
if __name__ == "__main__":
    # Crea un pipe (devuelve dos extremos: left y right)
    left, right = Pipe()
    # Ruta del fichero con los números
    ficherin = 'Tema2\\Ejercicio3\\numerines.txt'
    # Crea proceso que lee el fichero y envía por left
    p1 = Process(target=leer_numerines_de_fichero_muy_chulo, args=(left, ficherin))
    # Crea proceso que recibe por right y suma
    p2 = Process(target=suma_numerines, args=(right,))
    # Inicia el proceso lector
    p1.start()
    # Inicia el proceso sumador
    p2.start()
    # Marca tiempo de inicio
    start_time = time.time()
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