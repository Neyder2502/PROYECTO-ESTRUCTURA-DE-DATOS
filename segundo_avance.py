# Neyder Peña Codigo:2252004
# Julio Cesar Codigo: 2251503
# Diego Herazo Codigo: 2251704
# Santiago Cortes Codigo: 2251513
# Tomas Ramirez Codigo: 2251788

# En este codigo migramos de listas con prioridad a un sistema basado en arboles binarios, lo que mejora la eficiencia de busqueda y organizacion
# ademas agregamos una funcionalidad extra para mostrar la ocupacion de mesas de forma jerarquica, lo que puede ser util sobre todo para auditores

class NodoReserva:
    def __init__(self, cedula, nombre, personas, hora, mesas):
        # Datos base de la reserva
        self.cedula = int(cedula)
        self.nombre = nombre
        self.personas = personas
        self.hora = hora
        self.mesas = mesas
        # Punteros para la estructura de árbol
        self.izq = None
        self.der = None
        self.altura = 1 # necesario para calcular balanceo

class RestauranteArbol:
    def __init__(self):
        self.raiz = None  # Nodo raíz del árbol
        self.total_mesas = 20 # Capacidad total del restaurante
        self.mesas_por_hora = {h: 0 for h in range(4, 11)} # Diccionario 4pm-10pm

    # FUNCIONES DE APOYO AVL 
    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        return self.obtener_altura(nodo.izq) - self.obtener_altura(nodo.der) if nodo else 0

    def rotar_derecha(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        x.altura = 1 + max(self.obtener_altura(x.izq), self.obtener_altura(x.der))
        return x

    def rotar_izquierda(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        x.altura = 1 + max(self.obtener_altura(x.izq), self.obtener_altura(x.der))
        y.altura = 1 + max(self.obtener_altura(y.izq), self.obtener_altura(y.der))
        return y

    # INGRESAR RESERVA
    def ingresar_reserva(self, cedula, nombre, personas, hora):
        # Cálculo de mesas (1 mesa por cada 4 personas)
        mesas_necesarias = (personas + 3) // 4
        
        if hora < 4 or hora > 10:
            print("Horario no permitido (4pm a 10pm).")
            return

        # Validar disponibilidad de mesas
        if self.mesas_por_hora[hora] + mesas_necesarias > self.total_mesas:
            print(f"No hay mesas suficientes a las {hora}pm.")
            return

        def insertar(nodo, nuevo):
            if nodo is None:
                return nuevo
            if nuevo.cedula < nodo.cedula:
                nodo.izq = insertar(nodo.izq, nuevo)
            elif nuevo.cedula > nodo.cedula:
                nodo.der = insertar(nodo.der, nuevo)
            else:
                print("La cédula ya tiene una reserva activa.")
                return nodo

            # Actualizar altura y balancear
            nodo.altura = 1 + max(self.obtener_altura(nodo.izq), self.obtener_altura(nodo.der))
            balance = self.obtener_balance(nodo)

            # Casos de rotación para mantener AVL
            if balance > 1 and nuevo.cedula < nodo.izq.cedula: return self.rotar_derecha(nodo)
            if balance < -1 and nuevo.cedula > nodo.der.cedula: return self.rotar_izquierda(nodo)
            if balance > 1 and nuevo.cedula > nodo.izq.cedula:
                nodo.izq = self.rotar_izquierda(nodo.izq)
                return self.rotar_derecha(nodo)
            if balance < -1 and nuevo.cedula < nodo.der.cedula:
                nodo.der = self.rotar_derecha(nodo.der)
                return self.rotar_izquierda(nodo)
            return nodo

        nueva = NodoReserva(cedula, nombre, personas, hora, mesas_necesarias)
        self.raiz = insertar(self.raiz, nueva)
        
        # Bloquear mesas por 3 horas (política del restaurante)
        for h in range(hora, min(hora + 3, 11)):
            self.mesas_por_hora[h] += mesas_necesarias
        print("Reserva guardada exitosamente.")

    # CANCELAR RESERVA 
    def cancelar_reserva(self, cedula):
        cedula = int(cedula)
        
        def buscar_minimo(nodo):
            actual = nodo
            while actual.izq:
                actual = actual.izq
            return actual

        def eliminar(nodo, c):
            if nodo is None: return None
            
            if c < nodo.cedula:
                nodo.izq = eliminar(nodo.izq, c)
            elif c > nodo.cedula:
                nodo.der = eliminar(nodo.der, c)
            else:
                # Nodo encontrado: liberar mesas antes de borrar
                for h in range(nodo.hora, min(nodo.hora + 3, 11)):
                    self.mesas_por_hora[h] -= nodo.mesas
                
                # Caso 1 y 2: Un hijo o ninguno
                if nodo.izq is None: return nodo.der
                if nodo.der is None: return nodo.izq
                
                # Caso 3: Dos hijos (sucesor inorder)
                temp = buscar_minimo(nodo.der)
                nodo.cedula, nodo.nombre = temp.cedula, temp.nombre
                nodo.der = eliminar(nodo.der, temp.cedula)

            if nodo is None: return nodo

            # Re-balancear tras eliminar
            nodo.altura = 1 + max(self.obtener_altura(nodo.izq), self.obtener_altura(nodo.der))
            balance = self.obtener_balance(nodo)

            if balance > 1 and self.obtener_balance(nodo.izq) >= 0: return self.rotar_derecha(nodo)
            if balance < -1 and self.obtener_balance(nodo.der) <= 0: return self.rotar_izquierda(nodo)
            if balance > 1 and self.obtener_balance(nodo.izq) < 0:
                nodo.izq = self.rotar_izquierda(nodo.izq)
                return self.rotar_derecha(nodo)
            if balance < -1 and self.obtener_balance(nodo.der) > 0:
                nodo.der = self.rotar_derecha(nodo.der)
                return self.rotar_izquierda(nodo)
            return nodo

        self.raiz = eliminar(self.raiz, cedula)
        print(f"Proceso de cancelación terminado para CC: {cedula}.")

    # MIRAR MESAS DISPONIBLES
    def disponibilidad(self):
        print("\n   ESTADO DE MESAS ")
        for h, ocupadas in self.mesas_por_hora.items():
            print(f"Hora {h}pm: {self.total_mesas - ocupadas} disponibles.")

    # MOSTRAR RESERVAS (Recorrido Inorden)
    def mostrar_reservas(self):
        def inorden(nodo):
            if nodo:
                inorden(nodo.izq)
                print(f"CC: {nodo.cedula} | {nodo.nombre} | {nodo.hora}pm | Mesas: {nodo.mesas}")
                inorden(nodo.der)
        
        if not self.raiz:
            print("No hay reservas.")
        else:
            print("\n    LISTADO POR CÉDULA (ASCENDENTE) ")
            inorden(self.raiz)

    # BUSCAR RESERVA
    def buscar_reserva(self, cedula):
        def buscar(nodo, c):
            if nodo is None or nodo.cedula == c:
                return nodo
            if c < nodo.cedula:
                return buscar(nodo.izq, c)
            return buscar(nodo.der, c)

        res = buscar(self.raiz, int(cedula))
        if res:
            print(f"\nResultado: {res.nombre} - {res.personas} personas a las {res.hora}pm.")
        else:
            print("No se encontró ninguna reserva con esa cédula.")

    # CONTAR RESERVAS
    def contar_reservas(self):
        def contar(nodo):
            if nodo is None: return 0
            return 1 + contar(nodo.izq) + contar(nodo.der)
        
        total = contar(self.raiz)
        print(f"Total de reservas activas: {total}")

    # NUEVA FUNCIÓN: REPORTE POR NIVELES 
    def reporte_jerarquico(self):
        if not self.raiz:
            print("Árbol vacío.")
            return
        
        # Guardamos tuplas: (nodo, nivel_actual)
        cola = [(self.raiz, 1)] 
        print("\n   AUDITORÍA DE ESTRUCTURA POR NIVELES (AVL BALANCEADO)")
        
        while cola:
            nodo, nivel = cola.pop(0)
            print(f"[Nivel {nivel}] CC: {nodo.cedula} -> Cliente: {nodo.nombre}")
            # Al agregar a los hijos, les sumamos 1 al nivel del padre
            if nodo.izq: 
                cola.append((nodo.izq, nivel + 1))
            if nodo.der: 
                cola.append((nodo.der, nivel + 1))

# Menú Principal
def menu():
    sistema = RestauranteArbol()
    
    while True:
        print("\n    SISTEMA RESTAURANTE V2")
        print("1. Ingresar reserva")
        print("2. Cancelar reserva")
        print("3. Mesas disponibles")
        print("4. Mostrar reservas (Inorden)")
        print("5. Buscar reserva")
        print("6. Contar reservas")
        print("7. Reporte Jerárquico (Nueva Función)")
        print("8. Salir")

        opcion = input("Seleccione opcion: ")

        match opcion: 
            case "1":
                c = input("Cédula: ")
                n = input("Nombre: ")
                p = int(input("Personas: "))
                h = int(input("Hora (4-10): "))
                sistema.ingresar_reserva(c, n, p, h)
            case "2":
                c = input("Cédula a cancelar: ")
                sistema.cancelar_reserva(c)
            case "3":
                sistema.disponibilidad()
            case "4":
                sistema.mostrar_reservas()
            case "5":
                c = input("Cédula a buscar: ")
                sistema.buscar_reserva(c)
            case "6":
                sistema.contar_reservas()
            case "7":
                sistema.reporte_jerarquico()
            case "8":
                print("Saliendo..."); break
            case _:
                print("Opción inválida.")

if __name__ == "__main__":
    menu()