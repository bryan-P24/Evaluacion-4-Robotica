ALGORITMO Robot_Almacen

Mostrar menú

MIENTRAS el usuario no elija salir HACER

    Mostrar opciones:
        1. Entrega automática
        2. Control manual
        3. Ver almacén
        4. Salir

    Leer opción

    SEGÚN opción HACER

        CASO 1:
            Buscar paquete

            MIENTRAS existan paquetes HACER

                Calcular camino al paquete
                Mover robot al paquete
                Recoger paquete

                Calcular camino a zona de entrega
                Mover robot a zona de entrega
                Entregar paquete

            FIN MIENTRAS

        CASO 2:
            Mostrar almacén

            Pedir fila destino
            Pedir columna destino

            SI la posición es válida ENTONCES

                Calcular camino
                Mover robot al destino

                SI existe paquete ENTONCES
                    Recoger paquete

                    Preguntar si desea entregarlo

                    SI respuesta = "s" ENTONCES
                        Calcular camino a zona de entrega
                        Mover robot
                        Entregar paquete
                    FIN SI

                FIN SI

            SINO
                Mostrar error
            FIN SI

        CASO 3:
            Mostrar almacén

        CASO 4:
            Finalizar programa

        OTRO CASO:
            Mostrar "Opción inválida"

    FIN SEGÚN

FIN MIENTRAS

FIN ALGORITMO
