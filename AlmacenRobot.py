from collections import deque
import copy
import time

# El almacen es una cuadricula donde:
# 0 = espacio vacio
# 1 = obstaculo
# 2 = posicion inicial del robot
# 3 = paquete
# 4 = zona de entrega

ALMACEN = [
    [0, 0, 0, 1, 0],
    [0, 2, 0, 1, 3],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 3, 4],
]

INICIO = [1, 1]
ZONA_ENTREGA = [4, 4]

FILAS = len(ALMACEN)
COLS = len(ALMACEN[0])


def mostrar_almacen(almacen, robot, ruta=None, cargando=False):

    simbolos = {0: " . ", 1: "###", 3: "[P]", 4: "[E]"}

    pasos_ruta = set()
    if ruta:
        for p in ruta[1:-1]:
            pasos_ruta.add((p[0], p[1]))

    print("\n   " + "  ".join(str(c) for c in range(COLS)))

    for f in range(FILAS):
        linea = f"{f} |"
        for c in range(COLS):
            if [f, c] == robot:
                linea += "[r]" if cargando else "[R]"
            elif (f, c) in pasos_ruta:
                linea += " * "
            else:
                linea += simbolos.get(almacen[f][c], " . ")
        print(linea)

    print()


def buscar_paquete(almacen):

    for f in range(FILAS):
        for c in range(COLS):
            if almacen[f][c] == 3:
                return [f, c]

    return None


def buscar_camino(origen, destino, almacen):

    cola = deque([[origen]])
    visitados = {(origen[0], origen[1])}

    while cola:
        camino = cola.popleft()
        pos_actual = camino[-1]

        if pos_actual == destino:
            return camino

        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nf = pos_actual[0] + df
            nc = pos_actual[1] + dc

            dentro_del_mapa = 0 <= nf < FILAS and 0 <= nc < COLS

            if (
                dentro_del_mapa
                and almacen[nf][nc] != 1
                and (nf, nc) not in visitados
            ):
                visitados.add((nf, nc))
                cola.append(camino + [[nf, nc]])

    return None


def mover_robot(camino, almacen, pos, cargando=False):

    for paso in camino[1:]:
        pos[0] = paso[0]
        pos[1] = paso[1]

        estado = "cargando" if cargando else "vacio"

        print(
            f"Robot [{estado}] -> "
            f"fila {paso[0]}, columna {paso[1]}"
        )

        mostrar_almacen(almacen, pos, camino, cargando)

        time.sleep(0.3)


def entregar_paquetes():

    almacen = copy.deepcopy(ALMACEN)
    pos = list(INICIO)
    entregados = 0

    while True:

        paquete = buscar_paquete(almacen)

        if paquete is None:
            print(
                f"\nProceso terminado. "
                f"Paquetes entregados: {entregados}"
            )
            break

        print(f"\nPaquete encontrado en {paquete}")

        camino = buscar_camino(pos, paquete, almacen)

        if camino is None:
            print("No existe camino al paquete.")
            break

        mover_robot(camino, almacen, pos)

        almacen[paquete[0]][paquete[1]] = 0

        print("Paquete recogido.")

        camino = buscar_camino(
            pos,
            ZONA_ENTREGA,
            almacen
        )

        if camino is None:
            print("No existe camino a la zona de entrega.")
            break

        mover_robot(
            camino,
            almacen,
            pos,
            cargando=True
        )

        print("Paquete entregado.")
        entregados += 1


def mover_manual():

    almacen = copy.deepcopy(ALMACEN)
    pos = list(INICIO)

    while True:

        mostrar_almacen(almacen, pos)

        try:
            fila = int(input(f"Fila destino (0-{FILAS-1}): "))
            col = int(input(f"Columna destino (0-{COLS-1}): "))
        except ValueError:
            print("Ingrese numeros validos.")
            continue

        if not (0 <= fila < FILAS and 0 <= col < COLS):
            print("Posicion fuera del mapa.")
            continue

        if almacen[fila][col] == 1:
            print("Hay un obstaculo ahi.")
            continue

        camino = buscar_camino(
            pos,
            [fila, col],
            almacen
        )

        if camino is None:
            print("No existe camino a esa posicion.")
            continue

        mover_robot(camino, almacen, pos)

        print(f"Robot llego a [{fila}, {col}]")

        if almacen[fila][col] == 3:

            print("Hay un paquete aqui.")

            almacen[fila][col] = 0

            print("Paquete recogido.")

            opcion = input(
                "Llevar a zona de entrega? (s/n): "
            ).lower()

            if opcion == "s":

                camino = buscar_camino(
                    pos,
                    ZONA_ENTREGA,
                    almacen
                )

                if camino:

                    mover_robot(
                        camino,
                        almacen,
                        pos,
                        cargando=True
                    )

                    print("Paquete entregado.")

                else:
                    print(
                        "No existe camino a la zona de entrega."
                    )

        seguir = input(
            "\nMover el robot de nuevo? (s/n): "
        ).lower()

        if seguir != "s":
            break


def menu():

    while True:

        print("\n==========================")
        print("     ROBOT DE ALMACEN     ")
        print("==========================")
        print("1. Entrega automatica")
        print("2. Control manual")
        print("3. Ver almacen")
        print("4. Salir")

        opcion = input("\nElige una opcion: ")

        if opcion == "1":
            entregar_paquetes()

        elif opcion == "2":
            mover_manual()

        elif opcion == "3":
            mostrar_almacen(ALMACEN, INICIO)

        elif opcion == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    menu()