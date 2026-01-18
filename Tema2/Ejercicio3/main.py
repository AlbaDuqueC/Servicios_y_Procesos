from multiprocessing import Process, Queue
import time

def suma_numerines(numerin):
    suma = 0
    while True:
        n = numerin.get()
        if n is None:
            break
        suma += n
    print("Suma total del fichero:", suma)

def leer_numerines_de_fichero_muy_chulo(q, ruta_fichero):
    with open(ruta_fichero, 'rt') as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                q.put(int(linea))

    q.put(None)

if __name__ == "__main__":
    
    ficherin = 'Tema2\\Ejercicio3\\numerines.txt'
    queue = Queue()

    start_time = time.time()

    p1 = Process(target=leer_numerines_de_fichero_muy_chulo, args=(queue, ficherin))
    p2 = Process(target=suma_numerines, args=(queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end_time = time.time()
    print("Finiquitao")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
