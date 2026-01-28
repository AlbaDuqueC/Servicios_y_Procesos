
import multiprocessing
import time

"""Modifica el ejercicio anterior para usar un Pool para lanzar varios 
procesos de forma concurrente. Recuerda que al tener dos argumentos debes 
usar el método starmap en vez de map."""

# Función que suma todos los números entre a y b
def sumar_rango(a, b):
    # Obtiene el valor mínimo (inicio del rango)
    inicio_rango = min(a, b)
    # Obtiene el valor máximo (fin del rango)
    fin_rango = max(a, b)
    # Suma todos los números del rango
    suma = sum(range(inicio_rango, fin_rango + 1))
    # Imprime el resultado
    print(f"Suma rango [{inicio_rango}, {fin_rango}] = {suma}")
    # Retorna la suma (útil para Pool)
    return suma

# Función principal del ejercicio
def ejercicio_6():

    print ("EJERCICIO 6")

    # Lista de parejas de valores a procesar
    parejas= [(1, 1000000), (500, 100), (100, 2000000)]
    # Marca tiempo de inicio
    start= time.time()
    # Crea un Pool con 3 procesos trabajadores
    with multiprocessing.Pool(processes=3) as pool:
        # starmap distribuye la función con múltiples argumentos
        pool.starmap(sumar_rango, parejas)
    # Mensaje de finalización
    print("Todos los procesos del Pool han terminado.")
    # Calcula y muestra el tiempo transcurrido
    print(f"Tiempo Ej 6: {time.time() - start:.4f} seg\n")

# Protección para multiprocessing
if __name__ == "__main__":
    ejercicio_6()