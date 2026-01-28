from multiprocessing import Pool
import time

"""Modifica el ejercicio anterior para que el programa principal use un Pool para lanzar varios 
procesos de forma concurrente. Cambia el valor del número de procesos y compara los tiempos que 
tarda en ejecutarse en los distintos casos."""

# Función que suma números del 1 hasta n
def sumar_numeros(n):
    suma = 0
    # Suma todos los números desde 1 hasta n
    for i in range(1, n + 1):
        suma += i
    print(suma)

# Protección necesaria para multiprocessing
if __name__ == "__main__":
    # Pide un número al usuario
    numerin = int(input("Dime un numerin: "))
    # Marca el tiempo de inicio
    start_time=time.time()
    # Crea una lista con el valor a procesar
    valores = [numerin]
    # Crea un Pool con 1 proceso trabajador
    with Pool(processes=1) as pool:
        # Distribuye la función sumar_numeros sobre los valores
        pool.map(sumar_numeros, valores)
    # Mensaje indicando finalización
    print("Todos los procesos han terminado")
    # Marca el tiempo de fin
    end_time = time.time()
    # Calcula y muestra el tiempo total
    print(f"Tiempo total: {end_time - start_time:.4f} segundos")