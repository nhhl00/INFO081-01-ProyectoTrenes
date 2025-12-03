# INFO081-01-PROYECTO
# Informe: Sistema de Simulación de Tráfico Ferroviario para EFE Chile

El informe presenta el diseño de un sistema de simulación de tráfico ferroviario para EFE Chile, que modela el transporte de pasajeros, el movimiento de trenes y la gestión de eventos. Propone una arquitectura modular con clases para trenes, estaciones y pasajeros, además de un sistema de persistencia y una interfaz interactiva. Incluye diagramas y plantea futuras mejoras para ampliar la simulación.

## Integrantes
- Benjamin Martinez  
- Gustavo Martinez  
- Agustin Montenegro  
- Renzo Naglieri  

## Indicadores del Sistema
- **Cantidad de personas:** Este indicador nos indicará la cantidad de personas para ayudar al funcionamiento del tren.  
- **Vagones disponibles:** Este indicador nos indicará la cantidad de vagones disponibles según la cantidad de personas que estén en el tren.

## Almacenamiento y persistencia de datos
El sistema de guardado crea una instantánea del estado de la simulación en formato JSON y la organiza automáticamente en carpetas por fecha (año/mes/día). Cada archivo se nombra por la hora de creación (por ejemplo `guardado_HH-MM-SS.json`). El JSON contiene la hora de la simulación, los datos esenciales de estaciones, vías y trenes, la cola de eventos y un resumen de pasajeros activos. Desde la pestaña “Simulación” de la interfaz se puede guardar y cargar: al guardar se genera el archivo y se muestra su ruta; al cargar se selecciona un guardado, se restaura el estado (incluida la hora) y la UI se actualiza para reflejarlo. La serialización almacena principalmente datos representativos (diccionarios/IDs), por lo que la reconstrucción completa de objetos complejos puede requerir lógica adicional; se recomienda añadir metadatos/versionado y validar los archivos al cargar para asegurar compatibilidad futura.

## Archivos principales 
python main.py
para ejecutar nuestros archivos principales, los cuales tenga el nombre "main" se segurian los siguientes pasos 
- abrir un terminal
- posicionarse en la carpeta principal del proyecto
- cd INFO081-01-ProyectoTrenes/Proyecto_EFE
- ejecutar los archivos principales con los siguientes comandos:
- python main.py
## Decisiones de Diseño del Sistema Ferroviario 
- sentido de las vías
- Estado de los trenes como: "detenido" , "viajando"
- Capacidad de los bagones
- Cantidad de pasajeros
