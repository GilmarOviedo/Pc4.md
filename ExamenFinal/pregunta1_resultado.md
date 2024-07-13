
Importaciones y Configuración Inicial:

    Se importan los módulos necesarios para la programación asíncrona, registro de eventos, manejo de colas, ejecución de tareas en hilos y sincronización de hilos.

Clase Event:

    Representa un evento con un tipo, datos asociados y una prioridad.

Clase Notebook:

    Simula un cuaderno con celdas.
    Contiene un método asíncrono execute_cell que simula la ejecución de una celda con un retraso.

Clase EventSystem:

    Maneja la cola de eventos y la ejecución de celdas en el Notebook.
    Utiliza un Lock para asegurar operaciones seguras al acceder a la cola de eventos.
    Tiene métodos para agregar eventos, manejar eventos y ejecutar el bucle de eventos.

Función main:

    Crea una instancia de EventSystem.
    Agrega eventos de ejecución de celdas con diferentes prioridades.
    Inicia el bucle de eventos.

Punto de Entrada:

    Ejecuta la función principal main utilizando asyncio.run.

+--------------------+       +---------------------+
|    Notebook        |       |      EventSystem    |
+--------------------+       +---------------------+
| - cells: list      |       | - event_queue: deque|
| - state: dict      |       | - lock: Lock        |
+--------------------+       | - notebook: Notebook|
| + execute_cell()   |       +---------------------+
+--------------------+       | + add_event()       |
                             | + handle_event()    |
                             | + event_loop()      |
                             +---------------------+

         (1)                                      
     Add Event                                   
         +                                       
         |                                       
         v                                       
+--------------------+                           
|  EventQueue        |                           
|                    |                           
| - "execute Cell 1" |                           
| - "execute Cell 2" |                           
| - "execute Cell 3" |                           
+--------------------+                           
         |                                       
         v                                       
      Dequeue Event                             
         +                                       
         |                                       
         v                                       
+-------------------+   (2) Execution Order      
|   execute_cell()  |                           
| - "Cell 2"        |                           
| - "Cell 1"        |                           
| - "Cell 3"        |                           
+-------------------+ 

Flujo de Trabajo

    Adición de Eventos:
        Los eventos se agregan a la cola event_queue con sus respectivas prioridades utilizando add_event.

    Bucle de Eventos:
        event_loop desencola eventos según su prioridad y los maneja utilizando handle_event, que llama al método execute_cell del Notebook para ejecutar las celdas.

    Ejecución de Celdas:
        execute_cell simula la ejecución de una celda, registrando el inicio y finalización de la ejecución.



INFO:__main__:Evento agregado: execute - Celda 1 con prioridad 2
INFO:__main__:Evento agregado: execute - Celda 2 con prioridad 1
INFO:__main__:Evento agregado: execute - Celda 3 con prioridad 3
INFO:__main__:Ejecutando celda: Celda 2
INFO:__main__:Celda Celda 2 ejecutada con éxito
INFO:__main__:Ejecutando celda: Celda 1
INFO:__main__:Celda Celda 1 ejecutada con éxito
INFO:__main__:Ejecutando celda: Celda 3
INFO:__main__:Celda Celda 3 ejecutada con éxito





