from multiprocessing import Process, Queue, Pipe
import time

"""En este caso, vuelve a realizar la comunicación entre procesos pero usando tuberías (Pipe), 
de forma que la función que se encarga de leer los números del fichero se los envíe (send) al 
proceso que se encarga de la suma. El proceso que suma los números tiene que recibir (recv) un 
número y realizar la suma. Una vez que el proceso que lee el fichero termine de leer números en 
el fichero, debe enviar un None. El que recibe números dejará de realizar sumas cuando reciba 
un None."""

def suma_numerines(numerin):
    suma = 0
    while True:
        n = numerin.recv()
        if n is None:
            break
        suma += n
    print("Suma total del fichero:", suma)

def leer_numerines_de_fichero_muy_chulo(q, ruta_fichero):
    with open(ruta_fichero, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                q.send(int(linea))

    q.send(None)
    q.close()

if __name__ == "__main__":

    left, right = Pipe()

    ficherin = 'Tema2\\Ejercicio3\\numerines.txt'


    p1 = Process(target=leer_numerines_de_fichero_muy_chulo, args=(left, ficherin))
    p2 = Process(target=suma_numerines, args=(right,))

    p1.start()
    p2.start()
    start_time = time.time()

    p1.join()
    p2.join()

    end_time = time.time()
    print("Finiquitao")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
