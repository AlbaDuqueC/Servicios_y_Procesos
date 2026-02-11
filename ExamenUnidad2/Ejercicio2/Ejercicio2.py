import multiprocessing as mp

# PROCESO 1: Filtrar por departamento
def filtrar_departamento(departamento, conn_out):
    with open("salarios.txt", "r") as f:
        for linea in f:
            nombre, apellido, salario, dept = linea.strip().split(";")
            if dept == departamento:
                # Enviar sin el departamento
                conn_out.send(f"{nombre};{apellido};{salario}")
    conn_out.close()


# PROCESO 2: Filtrar por salario mínimo
def filtrar_salario(salario_min, conn_in, conn_out):
    while True:
        try:
            linea = conn_in.recv()
        except EOFError:
             print("Error")

        nombre, apellido, salario = linea.split(";")
        if int(salario) >= salario_min:
            conn_out.send(linea)

    conn_out.close()


# PROCESO 3: Escribir empleados.txt
def escribir_empleados(conn_in):
    with open("empleados.txt", "w") as f:
        while True:
            try:
                linea = conn_in.recv()
            except EOFError:
                print("Error")

            nombre, apellido, salario = linea.split(";")
            f.write(f"{apellido} {nombre}, {salario}\n")


# MAIN
def main_ej2():
    departamento = input("Introduce el departamento: ")
    salario_min = int(input("Introduce salario mínimo: "))

    # Pipes
    p1_out, p2_in = mp.Pipe()
    p2_out, p3_in = mp.Pipe()

    # Procesos
    p1 = mp.Process(target=filtrar_departamento, args=(departamento, p1_out))
    p2 = mp.Process(target=filtrar_salario, args=(salario_min, p2_in, p2_out))
    p3 = mp.Process(target=escribir_empleados, args=(p3_in,))

    # Lanzar
    p1.start()
    p2.start()
    p3.start()

    # Esperar
    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    main_ej2()
