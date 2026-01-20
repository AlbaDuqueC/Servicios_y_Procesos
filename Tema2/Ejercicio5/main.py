
"""Crea una función en Python que sea capaz de sumar todos los números comprendidos entre 
dos valores, incluyendo ambos valores y mostrar el resultado por pantalla. Estos valores se 
les pasará como argumentos. Hay que tener presente que el primer argumento puede ser mayor 
que el segundo, y habrá que tenerlo presente para realizar la suma."""

import multiprocessing
import time

def sumar_rango(a, b):

    inicio_rango = min(a, b)
    fin_rango = max(a, b)

    suma = sum(range(inicio_rango, fin_rango + 1))

    print("Suma rango: {suma}")

def ejercicio_5():
    print("EJERCICIO 5")
    parejas = [(1,1000000), (5000, 100), (10, 2000000)]
    procesos = []

    start = time.time()
    for p in parejas: 
        proc = multiprocessing.Process(target=sumar_rango, args=(p[0], p[1]))
        procesos.append(proc)
        proc.start()
    
    for proc in procesos:
        proc.join()
    
    print("Todos los procesos han terminado.") # [cite: 24]
    print(f"Tiempo Ej 5: {time.time() - start:.4f} seg\n")

if __name__ == "__main__":
    ejercicio_5()


