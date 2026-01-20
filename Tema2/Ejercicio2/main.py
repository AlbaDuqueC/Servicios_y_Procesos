from multiprocessing import Pool
import time

"""Modifica el ejercicio anterior para que el programa principal use un Pool para lanzar varios 
procesos de forma concurrente. Cambia el valor del número de procesos y compara los tiempos que 
tarda en ejecutarse en los distintos casos."""

def sumar_numeros(n):
    suma = 0

    for i in range(1, n + 1):
        suma += i
    print(suma)

if __name__ == "__main__":

    numerin = int(input("Dime un numerin: "))

    start_time=time.time()

    valores = [numerin]

    with Pool(processes=1) as pool:
        pool.map(sumar_numeros, valores)

    print("Todos los procesos han terminado")

    end_time = time.time()
    print(f"Tiempo total: {end_time - start_time:.4f} segundos")