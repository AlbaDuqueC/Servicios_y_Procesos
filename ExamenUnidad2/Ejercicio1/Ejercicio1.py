import multiprocessing as mp
import random
import os


# PROCESO 1: Generar temperaturas
def generar_temperaturas(dia):
    nombre = f"{dia:02d}-12.txt"
    with open(nombre, "w") as f:
        for _ in range(24):
            temp = round(random.uniform(0, 20), 2)
            f.write(str(temp) + "\n")


# PROCESO 2: Máximas
def calcular_maxima(dia):
    nombre = f"{dia:02d}-12.txt"
    with open(nombre, "r") as f:
        temps = [float(x) for x in f.readlines()]
    maxima = max(temps)
    with open("maximas.txt", "a") as f:
        f.write(f"{dia:02d}-12:{maxima}\n")


# PROCESO 3: Mínimas
def calcular_minima(dia):
    nombre = f"{dia:02d}-12.txt"
    with open(nombre, "r") as f:
        temps = [float(x) for x in f.readlines()]
    minima = min(temps)
    with open("minimas.txt", "a") as f:
        f.write(f"{dia:02d}-12:{minima}\n")

# Main
def main_ej1():
    # 1. Lanzar 31 procesos para generar temperaturas
    procesos = []
    for dia in range(1, 32):
        p = mp.Process(target=generar_temperaturas, args=(dia,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    # 2. Procesos para máximas
    procesos = []
    for dia in range(1, 32):
        p = mp.Process(target=calcular_maxima, args=(dia,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    # 3. Procesos para mínimas
    procesos = []
    for dia in range(1, 32):
        p = mp.Process(target=calcular_minima, args=(dia,))
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()


if __name__ == "__main__":
    main_ej1()
