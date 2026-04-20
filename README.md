# Sistema de Gestión de Reservas - Restaurante V2


## Notion

El enlace al Notion se encuentra a continuacion:

[![Notion](https://img.shields.io/badge/Documentación_del_Proyecto-000000?style=for-the-badge&logo=notion&logoColor=white)](https://www.notion.so/SISTEMA-DE-RESERVAS-DE-UN-RESTAURANTE-2ffd914b0c91805bafa6d94f9ea1bd91)


## Integrantes

* **Neyder Peña** - Cod: 2252004
* **Julio Cesar** - Cod: 2251503
* **Diego Herazo** - Cod: 2251704
* **Santiago Cortes** - Cod: 2251513
* **Tomas Ramirez** - Cod: 2251788

Este proyecto es un sistema de gestión de reservas diseñado para un restaurante con una capacidad de 20 mesas, operando en un horario de 4:00 PM a 10:00 PM. 

La aplicación permite administrar clientes, validar disponibilidad en tiempo real y asegurar una organización eficiente mediante algoritmos avanzados.


## Evolución del Proyecto

El sistema ha pasado por dos fases críticas de desarrollo:

1.  **Fase 1 (Listas Enlazadas):** 
	Implementación inicial utilizando colas con prioridad para organizar reservas por hora.
2.  **Fase 2 (Árboles AVL):** 
	Optimización total del sistema migrando a un Árbol Binario de Búsqueda Balanceado (AVL). Esto redujo la complejidad de búsqueda de $O(n)$ a $O(\log n)$, garantizando rapidez incluso con miles de registros.

## Características Principales

* **Ingreso Inteligente:** Registro de clientes con auto-balanceo de la estructura (Rotaciones AVL).
* **Gestión de Mesas:** Cálculo automático de mesas necesarias (1 mesa cada 4 personas) y bloqueo de disponibilidad por 3 horas.
* **Auditoría Técnica:** Función de reporte jerárquico para visualizar la salud y equilibrio del árbol por niveles.
* **Búsqueda Ultra-rápida:** Localización de reservas mediante el número de cédula.


## Tecnologías Utilizadas

* **Lenguaje:** Python 3.13
* **Estructuras:** * Árboles AVL (Balanceo por altura).
    * Diccionarios para gestión horaria.
    * Algoritmos de recorrido (Inorden y BFS).