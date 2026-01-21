
import multiprocessing
import time

"""En este caso, vuelve a realizar la comunicación entre procesos pero usando 
tuberías (Pipe), de forma que la función que se encarga de leer los números del 
fichero se los envíe (send) al proceso que los suma. El proceso que suma los 
números tiene que recibir (recv) los dos números y realizar la suma entre ellos.
"""

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

# Función que lee pares del fichero y los envía por el pipe
def leer_pares_pipe(nombre_archivo, conn):
    try:
        # Abre el fichero en modo lectura
        with open(nombre_archivo, 'r') as f:
            # Recorre cada línea
            for linea in f:
                # Divide la línea por espacios
                numeros = linea.strip().split()
                # Si hay exactamente 2 números
                if len(numeros) == 2:
                    # Crea tupla con los dos números
                    par = (int(numeros[0]), int(numeros[1]))
                    # Envía la tupla por el pipe
                    conn.send(par)
        # Envía None para indicar fin
        conn.send(None)
        print(f"Lectura de pares completada de {nombre_archivo}")
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado")
        # Envía None aunque haya error
        conn.send(None)
    finally:
        # Cierra la conexión del pipe
        conn.close()

# Función que recibe pares del pipe y suma los rangos
def sumar_pares_pipe(conn):
    suma_total = 0
    contador = 0
    # Bucle infinito hasta recibir None
    while True:
        # Recibe un par del pipe
        par = conn.recv()
        # Si recibe None, termina
        if par is None:
            break
        # Desempaqueta la tupla
        inicio, fin = par
        # Suma el rango y guarda el resultado
        resultado = sumar_rango(inicio, fin)
        # Acumula el resultado
        suma_total += resultado
        # Incrementa contador
        contador += 1
    # Imprime resumen
    print(f"Total de {contador} rangos procesados. Suma acumulada: {suma_total}")
    # Cierra la conexión del pipe
    conn.close()
    return suma_total

# Función principal del ejercicio
def ejercicio_8():
    print("\n=== EJERCICIO 8: Pares de números con Pipe ===")
    # Crea archivo de ejemplo con pares de números
    with open('num.txt', 'w') as f:
        f.write("1 100\n50 150\n200 300\n400 500\n")
    # Marca tiempo de inicio
    inicio = time.time()
    # Crea un pipe (dos extremos de comunicación)
    conn_recv, conn_send = multiprocessing.Pipe()
    # Crea proceso que lee fichero y envía por conn_send
    p_lector = multiprocessing.Process(target=leer_pares_pipe, args=('num.txt', conn_send))
    # Crea proceso que recibe por conn_recv y suma
    p_sumador = multiprocessing.Process(target=sumar_pares_pipe, args=(conn_recv,))
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
    print(f"Tiempo con Pipe: {fin - inicio:.4f} segundos\n")

# Protección para multiprocessing
if __name__ == "__main__":
    ejercicio_8()