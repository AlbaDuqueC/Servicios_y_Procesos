"""Realiza el ejercicio anterior pero esta vez va a haber otra función que 
lea los números de un fichero. En el fichero habrá dos números por línea 
separados por un espacio. En este caso, tienes que llevar a cabo una 
comunicación entre los dos procesos utilizando colas (Queue), de forma que 
la función que se encarga de leer los números los guarde en la cola, y la 
función que realiza la suma, recibirá la cola y tomará de ahí los dos 
números."""

import multiprocessing
import time

# Función que suma todos los números entre a y b
def sumar_rango(a, b):
    # Obtiene el valor mínimo
    inicio_rango = min(a, b)
    # Obtiene el valor máximo
    fin_rango = max(a, b)
    # Suma todos los números del rango
    suma = sum(range(inicio_rango, fin_rango + 1))
    # Imprime el resultado
    print(f"Suma rango [{inicio_rango}, {fin_rango}] = {suma}")
    # Retorna la suma
    return suma

# Función que lee pares de números del fichero y los mete en la cola
def leer_pares_queue(nombre_archivo, cola):
    try:
        # Abre el fichero en modo lectura
        with open(nombre_archivo, 'r') as f:
            # Recorre cada línea
            for linea in f:
                # Divide la línea por espacios
                numeros = linea.strip().split()
                # Si hay exactamente 2 números
                if len(numeros) == 2:
                    # Crea tupla con los dos números convertidos a enteros
                    par = (int(numeros[0]), int(numeros[1]))
                    # Mete la tupla en la cola
                    cola.put(par)
        # Mete None para indicar fin
        cola.put(None)
        print(f"Lectura de pares completada de {nombre_archivo}")
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado")
        # Mete None aunque haya error
        cola.put(None)

# Función que lee pares de la cola y suma los rangos
def sumar_pares_queue(cola):
    suma_total = 0
    contador = 0
    # Bucle infinito hasta recibir None
    while True:
        # Obtiene un par de la cola
        par = cola.get()
        # Si recibe None, termina
        if par is None:
            break
        # Desempaqueta la tupla
        inicio, fin = par
        # Suma el rango y guarda el resultado
        resultado = sumar_rango(inicio, fin)
        # Acumula el resultado
        suma_total += resultado
        # Incrementa contador de rangos procesados
        contador += 1
    # Imprime resumen
    print(f"Total de {contador} rangos procesados. Suma acumulada: {suma_total}")
    return suma_total

# Función principal del ejercicio
def ejercicio_7():
    print("\n=== EJERCICIO 7: Pares de números con Queue ===")
    # Crea archivo de ejemplo con pares de números
    with open('num.txt', 'w') as f:
        f.write("1 100\n50 150\n200 300\n400 500\n")
    # Marca tiempo de inicio
    inicio = time.time()
    # Crea una cola para comunicación
    cola = multiprocessing.Queue()
    # Crea proceso que lee el fichero y mete en la cola
    p_lector = multiprocessing.Process(target=leer_pares_queue, args=('num.txt', cola))
    # Crea proceso que lee de la cola y suma
    p_sumador = multiprocessing.Process(target=sumar_pares_queue, args=(cola,))
    # Inicia proceso lector
    p_lector.start()
    # Inicia proceso sumador
    p_sumador.start()
    # Espera a que termine el lector
    p_lector.join()
    # Espera a que termine el sumador
    p_sumador.join()
    # Marca tiempo de fin
    fin = time.time()
    # Calcula y muestra el tiempo transcurrido
    print(f"Tiempo con Queue: {fin - inicio:.4f} segundos\n")

# Protección para multiprocessing
if __name__ == "__main__":
    ejercicio_7()