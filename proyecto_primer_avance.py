# Neyder Peña Codigo:2252004
# Julio Cesar Codigo: 2251503
# Diego Herazo Codigo: 2251704
# Santiago Cortes Codigo: 2251513
# Tomas Ramirez Codigo: 2251788

# El codigo esta bastante comentado porque mientras lo iba haciendo lo iba explicando para que todos entendieran
# Como una especie de repaso para el parcial :D

class Nodo:
    # el class es para definir un modelo para crear objetos
    def __init__(self, cedula, nombre, personas, hora, mesas):  # informacion y cantidad de mesas
        # el init define como va a inicializar el nodo
        self.cedula = cedula
        self.nombre = nombre
        self.personas = personas
        self.hora = hora
        self.mesas = mesas
        self.prioridad = hora  # la prioridad va a ser la hora mas cercana
        self.siguiente = None

class Restaurante:
    def __init__(self): # esto es para inicializar el sistema
        self.cabeza = None
        self.total_mesas = 20
        self.mesas_por_hora = {4:0,5:0,6:0,7:0,8:0,9:0,10:0} # para conteo de mesas/hora

    # Registro de reserva
    def ingresar_reserva(self, cedula, nombre, personas, hora):
        while hora < 4 or hora > 10: # sencillo, es validar
            print("Horario invalido")
            hora = int(input("Ingrese una hora valida (4-10): "))
        mesas_necesarias = (personas + 3) // 4 # calcula las mesas necesarias (redondea hacia arriba)
        h = hora # vamos a mirar si la mesa esta dispoible las 3 horas
        while h < hora + 3:
            if h < 10:
                break
            if self.mesas_por_hora[h] + mesas_necesarias > self.total_mesas: # si en alguna hora no hay mesas suficientes, no se puede reservar
                print("\nNo hay mesas disponibles para ese horario")
                return
            h += 1
        nuevo = Nodo(cedula, nombre, personas, hora, mesas_necesarias)
        if self.cabeza is None or nuevo.prioridad < self.cabeza.prioridad: # por si esta vacia o tiene mayor prioridad
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            h = hora
            while h < hora + 3:
                self.mesas_por_hora[h] += mesas_necesarias
                h += 1 
            print("\nReserva registrada")
            return
        actual = self.cabeza # recorrido para encontrar su lugar
        while actual.siguiente is not None and actual.siguiente.prioridad <= nuevo.prioridad:
            actual = actual.siguiente
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        h = hora # para ocupar mesas
        while h < hora + 3:
            self.mesas_por_hora[h] += mesas_necesarias
            h += 1
        print("\nReserva registrada")
    
    # Cancelar reserva
    def cancelar_reserva(self, cedula):
        if self.cabeza is None: # lo mismo, validamos primero
            print("\nNo hay reservas")
            return
        if self.cabeza.cedula == cedula: # si esta en el primer lugar
            eliminado = self.cabeza
            self.cabeza = self.cabeza.siguiente
            h = eliminado.hora
            while h < eliminado.hora + 3: # liberamos las mesas
                self.mesas_por_hora[h] -= eliminado.mesas
                h += 1
            print("\nReserva cancelada")
            return
        actual = self.cabeza # recorrido para encontrar la reserva que vamos a quitar
        while actual.siguiente is not None and actual.siguiente.cedula != cedula:
            actual = actual.siguiente
        if actual.siguiente is None:
            print("\nNo hay reserva con esa cedula")
            return
        eliminado = actual.siguiente
        actual.siguiente = actual.siguiente.siguiente
        h = eliminado.hora
        while h < eliminado.hora + 3: # volvemos a liberar
            self.mesas_por_hora[h] -= eliminado.mesas
            h += 1
        print("\nReserva cancelada")

    # disponibilidad de mesas
    def disponibilidad(self):
        print("\nMesas disponibles por horario:")
        hora = 4 # la hora minima es 4
        while hora <= 10: # recorremos hasta la ultima hora
            ocupadas = self.mesas_por_hora[hora]
            libres = self.total_mesas - ocupadas
            print("\n")
            print("Hora: ", hora, "/ Mesas libres: ", libres)
            hora += 1

    # mostrar reservas
    def mostrar_reservas(self):
        if self.cabeza is None: # validamos
            print("\nNo hay reservas")
            return
        actual = self.cabeza # recorremos
        while actual is not None:
            print("\nCedula:", actual.cedula)
            print("Nombre:", actual.nombre)
            print("Personas:", actual.personas)
            print("Hora:", actual.hora)
            print("Mesas:", actual.mesas)
            actual = actual.siguiente

    # Buscar reserva
    def buscar_reserva(self, cedula):
        actual = self.cabeza
        while actual is not None:
            if actual.cedula == cedula:
                print("\nReserva encontrada")
                print("Nombre:", actual.nombre)
                print("Hora:", actual.hora)
                return
            actual = actual.siguiente
        print("\nNo hay reserva con esa cedula")

    # Contador reservas
    def contar_reservas(self):
        if self.cabeza is None: # validamos
            print("\nNo hay reservas")
            return
        contador = 0 # iniciamos contador y empezamos a recorrer
        actual = self.cabeza
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        print("\nTotal de reservas:", contador)

# Menu
def menu():
    sistema = Restaurante()
    while True:

        print("\n   SISTEMA DE RESERVAS    ")
        print("1. Ingresar reserva")
        print("2. Cancelar reserva")
        print("3. Mesas disponibles")
        print("4. Mostrar reservas")
        print("5. Buscar reserva")
        print("6. Contar reservas")
        print("7. Salir")

        while True: # esto es para que sea numero (tambien lo deberiamos poner en todos los datos numericos pero bueno)
            try:
                opcion = input("Seleccione opcion: ")
                break
            except ValueError:
                print("Ingrese un numero valido.")

        match opcion:

            case "1":
                cedula = input("Cedula: ")
                nombre = input("Nombre: ")
                personas = int(input("Personas: "))
                hora = int(input("Hora (4-10): "))
                sistema.ingresar_reserva(cedula, nombre, personas, hora)

            case "2":
                cedula = input("Cedula: ")
                sistema.cancelar_reserva(cedula)

            case "3":
                sistema.disponibilidad()

            case "4":
                sistema.mostrar_reservas()

            case "5":
                cedula = input("Cedula: ")
                sistema.buscar_reserva(cedula)

            case "6":
                sistema.contar_reservas()

            case "7":
                print("Saliendo...")
                break

            case _:
                print("Opcion invalida")

if __name__ == "__main__":
    menu()