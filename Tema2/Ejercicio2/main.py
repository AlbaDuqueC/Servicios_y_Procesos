from multiprocessing import Pool
import time

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