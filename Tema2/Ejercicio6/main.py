import multiprocessing
import time

"""Modifica el ejercicio anterior para usar un Pool para lanzar varios 
procesos de forma concurrente. Recuerda que al tener dos argumentos debes 
usar el método starmap en vez de map."""

# Función para sumar rango entre dos valores [cite: 21]
def sumar_rango(a, b):
    # Controlar si el primero es mayor que el segundo 
    inicio_rango = min(a, b)
    fin_rango = max(a, b)
    
    suma = sum(range(inicio_rango, fin_rango + 1))
    print(f"Suma rango [{inicio_rango}, {fin_rango}] = {suma}")
    return suma

def ejercicio_6():

    print ("EJERCICIO 6")

    parejas= [(1, 1000000), (500, 100), (100, 2000000)]

    start= time.time()
    with multiprocessing.Pool(processes=3) as pool:
        # Usar starmap para múltiples argumentos 
        pool.starmap(sumar_rango, parejas)
        
    print("Todos los procesos del Pool han terminado.")
    print(f"Tiempo Ej 6: {time.time() - start:.4f} seg\n")

if __name__ == "__main__":
    ejercicio_6()