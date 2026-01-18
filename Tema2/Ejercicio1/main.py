from multiprocessing import Process
import time

"""                         
            Crea una función en Python que sea capaz de sumar todos los números 
            desde el 1 hasta un valor introducido por parámetro, incluyendo ambos valores y mostrar el resultado por pantalla.
            Desde el programa principal crea varios procesos que ejecuten la función anterior. El programa principal 
            debe imprimir un mensaje indicando que todos los procesos han terminado después de que los procesos hayan impreso el resultado.
"""

def sumar_numeros(n):
    suma = 0

    for i in range(1, n + 1):
        suma += i
    print(suma)

if __name__ == "__main__":

    numerin = int(input("Dime un numerin: "))

    start_time=time.time()

    p = Process(target=sumar_numeros, args=(numerin,))

    p.start()

    end_time = time.time()
    print(f"Tiempo total: {end_time - start_time:.4f} segundos")