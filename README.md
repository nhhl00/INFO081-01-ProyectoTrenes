# INFO081-01-PROYECTO
# Informe: Sistema de Simulación de Tráfico Ferroviario para EFE Chile

El informe presenta el diseño de un sistema de simulación de tráfico ferroviario para EFE Chile, que modela el transporte de pasajeros, el movimiento de trenes y la gestión de eventos. Propone una arquitectura modular con clases para trenes, estaciones y pasajeros, además de un sistema de persistencia y una interfaz interactiva. Incluye diagramas y plantea futuras mejoras para ampliar la simulación.

## Integrantes
- Benjamin Martinez (OmeroSinson)
- Gustavo Martinez (Gustabio)
- Agustin Montenegro  (nhhl00)
- Renzo Naglieri  (v9z8mrgd9c)

## Indicadores del Sistema
- **Cantidad de personas:** Este indicador nos indicará la cantidad de personas en un tren para ayudar al funcionamiento del tren, apareciendo en la ui como un numero que cambiaria segun esa cantidad.
- **Vagones disponibles:** Este indicador nos indicará los vagones disponibles según la cantidad de personas que estén en el tren, mostrandose en la ui junto a los trenes.

## Almacenamiento y persistencia de datos
El sistema de guardado crea una instantánea del estado de la simulación en formato JSON y la organiza automáticamente en carpetas por fecha (año/mes/día).
- **Nombre del Archivo:** Se nombra por la hora de creación (por ejemplo, guardado_HH-MM-SS.json).
- **Contenido del JSON:** Contiene la hora de la simulación, los datos esenciales de estaciones, vías y trenes, la cola de eventos y un resumen de pasajeros activos.
- **Funcionalidad de la Interfaz:** Desde la pestaña "Simulación" de la interfaz se puede guardar y cargar:
- Al guardar se genera el archivo y se muestra su ruta.
- Al cargar se selecciona un guardado, se restaura el estado (incluida la hora) y la UI se actualiza para reflejarlo.
- **Serialización:** La serialización almacena principalmente datos representativos (diccionarios/IDs).

## Archivos principales 
python main.py
para ejecutar nuestros archivos principales, los cuales tenga el nombre "main" se segurian los siguientes pasos 
- Abrir un terminal
- Posicionarse en la carpeta principal del proyecto: 
- cd INFO081-01-ProyectoTrenes/Proyecto_EFE
- Ejecutar los archivos principales con los siguientes comandos:
- python main.py
  
## Decisiones de Diseño del Sistema Ferroviario 
- Estado de los trenes como: "detenido" , "viajando".
- Capacidad de los vagones: tienen su propia capacidad (capacidad_tren/2, en caso de ser 2 vagones).
- Estado de las vias como: "ocupada" , "desocupada".
- Canvas de la simulacion: el canvas se basa en rectangulos que representan a las estaciones, y lineas que representan a vias y rutas.
- UI de gestion: se integraron labels con la informacion de las Estaciones, Trenes y Vias en la pantalla de simulacion, y enlistar sus datos en estructuras de datos.
- Sistema de guardado: utilizando principalmente la libreria de python JSON para guardar datos.
- Pestañas: como principal metodo para cambiar a traves de las pantallas (partes) de la simulacion utilizando notebooks.

## Entidades
Se crearon diversas entidades u clases las cuales son:
- **Estaciones**: entidad diseñada para tener parametros y funciones necesarias para la poblacion (generacion de demanda), vias, rutas de trenes, etc.
- **Trenes**: entidad en la que se dan parametros e informcaion base a los trenes (ej: rutas) y funciones necesarias para el avance de trenes en la simulacion.
- **Vias**: entidad diseñada segun la informacion base de la simulacion, para contener las caracteristicas de vias, conexciones entre estaciones, estado segun el ocupamiento de la Via, y tiempo de recorrido de trenes.
- **Pasajero**: entidad para pasajeros que les otorga sus caracteristicas como id, origen, destino y tiempo de generacion en la simulacion.
- **HoraActual**: se asigna la fecha base y funciones necesarias para el avance de la hora en tiempo real, ademas de @property para obtener atributos de la hora de forma mas simple.
- **EstadoSimulacion**: clase en la que se encapsula la logica de generacion de demanda en las estaciones, rutas de pasajeros y logica de eventos.
- **GeneradorPersonas**: clase encargada de heredar la clase Generador, para la logica de generacion de clientes.
- **SistemaGuardado**: clase en la que se implementa el sistema de guardado utilizando JSON, con funciones para guardar el estado de simulacion (trenes,vias,estaciones,tiempo) y crear la rutas de guardado y carga.
- **Pestañas**: clase importante en la que se implemento la mayoria de codigo necesario para la creacion del ui, funciones para conectar las entidades, avance del reloj, eventos, etc. Asi como atributos para los frames.

## Eventos
Existen dos clases diseñadas para los eventos:
- **eventos**: clase a la que se le otorgan los atributos principales como tiempo, tipo, datos y id.
- **GestorEventos**: clase encargada de tener las funciones relacionadas a eventos, como lo es buscar estaciones y vias para que los trenes se muevan, la lista de eventos, la eliminacion de eventos por parte del usuario, etc.

