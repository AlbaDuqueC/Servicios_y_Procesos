from multiprocessing import Process  
import time 

"""                         
Crea una función en Python que sea capaz de sumar todos los números 
desde el 1 hasta un valor introducido por parámetro, incluyendo ambos valores y mostrar el resultado por pantalla.
Desde el programa principal crea varios procesos que ejecuten la función anterior. El programa principal 
debe imprimir un mensaje indicando que todos los procesos han terminado después de que los procesos hayan impreso el resultado.
"""
 # Define la función que suma números del 1 hasta n
def sumar_numeros(n): 

     # Inicializa la variable suma en 0
    suma = 0 

     # Bucle que itera desde 1 hasta n (inclusive)
    for i in range(1, n + 1): 
        suma += i  
    print(f"Suma hasta {n}: {suma}")  

# Protección necesaria para multiprocessing, ejecuta solo si es el programa principal
if __name__ == "__main__":  

    # Lista con varios números para crear varios procesos
    valores = [1000, 5000, 10000, 50000]  

    # Lista vacía para guardar todos los procesos creados
    procesos = []  
    
    
    # Crear y lanzar varios procesos
    for num in valores:  

         # Crea un proceso que ejecutará sumar_numeros con num como argumento
        p = Process(target=sumar_numeros, args=(num,)) 

        # Añade el proceso a la lista de procesos
        procesos.append(p)  

        # Inicia la ejecución del proceso (lanza el proceso hijo)
        p.start()  
    
    # Esperar a que TODOS los procesos terminen
    for p in procesos:  

        # Bloquea la ejecución hasta que el proceso p termine completamente
        p.join()  
    
    # Guarda el tiempo actual en segundos (marca de fin)
    end_time = time.time()  

    # Mensaje indicando que todos los procesos finalizaron
    print("Todos los procesos han terminado")  
    