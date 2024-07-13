import asyncio  # Importa el módulo asyncio para la programación asíncrona.
import logging  # Importa el módulo logging para el registro de eventos.
from collections import deque  # Importa deque para manejar la cola de eventos.
from concurrent.futures import ThreadPoolExecutor  # Importa ThreadPoolExecutor para ejecutar tareas en hilos.
from threading import Lock  # Importa Lock para asegurar operaciones seguras en hilos.

# Configuración básica del registro de eventos.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Clase que representa un evento.
class Event:
    def __init__(self, event_type, data, priority=1):
        self.event_type = event_type  # Tipo de evento (por ejemplo, "execute").
        self.data = data  # Datos asociados con el evento.
        self.priority = priority  # Prioridad del evento (valor por defecto es 1).

# Clase que simula un cuaderno (notebook) con celdas para ejecutar.
class Notebook:
    def __init__(self):
        self.cells = []  # Lista de celdas (vacía en este caso).
        self.state = {}  # Diccionario para almacenar el estado de cada celda.

    # Método asíncrono para ejecutar una celda.
    async def execute_cell(self, cell):
        logger.info(f"Ejecutando celda: {cell}")  # Registro de inicio de ejecución de la celda.
        await asyncio.sleep(1)  # Simula el tiempo de ejecución de la celda.
        self.state[cell] = "Ejecutada"  # Actualiza el estado de la celda a "Ejecutada".
        logger.info(f"Celda {cell} ejecutada con éxito")  # Registro de finalización de la ejecución de la celda.

# Clase principal que maneja los eventos.
class EventSystem:
    def __init__(self):
        self.event_queue = deque()  # Cola de eventos.
        self.lock = Lock()  # Lock para asegurar operaciones seguras en hilos.
        self.notebook = Notebook()  # Instancia de la clase Notebook.
        self.executor = ThreadPoolExecutor()  # Crea un ThreadPoolExecutor para ejecutar tareas en hilos.

    # Método para agregar eventos a la cola.
    def add_event(self, event):
        with self.lock:  # Bloquea el acceso a la cola para operaciones seguras en hilos.
            self.event_queue.append(event)  # Agrega el evento a la cola.
            self.event_queue = deque(sorted(self.event_queue, key=lambda e: e.priority))  # Ordena la cola por prioridad.
            logger.info(f"Evento agregado: {event.event_type} - {event.data} con prioridad {event.priority}")  # Registro del evento agregado.

    # Método asíncrono para manejar un evento.
    async def handle_event(self, event):
        try:
            if event.event_type == "execute":  # Si el tipo de evento es "execute".
                await self.notebook.execute_cell(event.data)  # Ejecuta la celda.
            else:
                logger.warning(f"Tipo de evento desconocido: {event.event_type}")  # Registro de advertencia si el tipo de evento es desconocido.
        except Exception as e:  # Manejo de excepciones.
            logger.error(f"Error manejando el evento {event}: {e}")  # Registro del error.

    # Bucle asíncrono que procesa los eventos en la cola.
    async def event_loop(self):
        while True:  # Bucle infinito.
            if self.event_queue:  # Si hay eventos en la cola.
                with self.lock:  # Bloquea el acceso a la cola para operaciones seguras en hilos.
                    event = self.event_queue.popleft()  # Desencola el primer evento.
                await self.handle_event(event)  # Maneja el evento.
            else:
                await asyncio.sleep(0.1)  # Espera 0.1 segundos para evitar busy waiting.

# Función principal asíncrona.
async def main():
    event_system = EventSystem()  # Crea una instancia de EventSystem.
    
    # Simulación de eventos
    event_system.add_event(Event("execute", "Celda 1", priority=2))  # Agrega evento para ejecutar "Celda 1".
    event_system.add_event(Event("execute", "Celda 2", priority=1))  # Agrega evento para ejecutar "Celda 2".
    event_system.add_event(Event("execute", "Celda 3", priority=3))  # Agrega evento para ejecutar "Celda 3".
    
    await event_system.event_loop()  # Inicia el bucle de eventos.

# Punto de entrada del script.
if __name__ == "__main__":
    asyncio.run(main())  # Ejecuta la función principal asíncrona.

