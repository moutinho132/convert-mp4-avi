# Requirements Document

## Introduction

El Conversor de MP4 a AVI es un sistema web de conversión de video que permite a los usuarios convertir archivos de video del formato MP4 al formato AVI. El sistema proporciona una interfaz web amigable para explorar directorios fuente, seleccionar múltiples archivos MP4 y convertirlos en lote al formato AVI. La aplicación está construida con una arquitectura hexagonal (Ports & Adapters) usando Python con FastAPI en el backend y React con Material-UI en el frontend, containerizada mediante Docker para facilitar el despliegue y la escalabilidad.

## Glossary

- **Sistema_Conversor**: La aplicación completa de conversión de video incluyendo frontend, backend y motor de conversión
- **Interfaz_Web**: La interfaz web basada en React con Material-UI para la interacción del usuario
- **Motor_Conversion**: El componente basado en FFmpeg responsable de la conversión de formato de video
- **Directorio_Fuente**: La ruta del directorio donde se encuentran los archivos MP4 para conversión
- **Directorio_Destino**: La ruta del directorio donde se guardan los archivos AVI convertidos
- **Conversion_Lote**: El proceso de convertir múltiples archivos MP4 simultáneamente
- **Trabajo_Conversion**: Una sola tarea de conversión para un archivo MP4
- **Cola_Conversion**: La cola que gestiona los trabajos de conversión pendientes
- **Contenedor_Docker**: El entorno de ejecución containerizado para el Sistema_Conversor
- **FastAPI**: Framework web moderno de Python de alto rendimiento para construir APIs con documentación automática y tipado nativo
- **Arquitectura_Hexagonal**: Patrón de arquitectura de software también conocido como Ports & Adapters que separa el dominio de la infraestructura
- **Capa_Dominio**: Capa central de la arquitectura hexagonal que contiene la lógica de negocio pura y entidades
- **Capa_Aplicacion**: Capa que contiene los casos de uso y orquesta el flujo entre el dominio y la infraestructura
- **Capa_Infraestructura**: Capa externa que contiene adaptadores para bases de datos, APIs externas y otros servicios
- **Puerto**: Interfaz que define cómo se comunica el dominio con el mundo exterior
- **Adaptador**: Implementación concreta de un puerto que conecta con servicios externos
- **Material_UI**: Librería de componentes React que implementa el diseño Material Design de Google
- **Microservicio**: Arquitectura donde el Sistema_Conversor opera como un servicio independiente, stateless y contenedorizado

## Requirements

### Requisito 1: Interfaz de Usuario Web

**Historia de Usuario:** Como usuario, quiero una interfaz web para interactuar con el sistema de conversión, para poder explorar y convertir archivos de video fácilmente sin conocimientos técnicos.

#### Criterios de Aceptación

1. CUANDO un usuario navega a la URL de la aplicación, LA Interfaz_Web DEBERÁ cargar y mostrar un explorador de archivos mostrando los archivos MP4 disponibles en el Directorio_Fuente dentro de 3 segundos
2. LA Interfaz_Web DEBERÁ proporcionar controles para seleccionar o deseleccionar archivos MP4 individuales para conversión, con un máximo de 1000 archivos mostrados simultáneamente
3. LA Interfaz_Web DEBERÁ proporcionar un botón para seleccionar todos los archivos MP4 visibles, y un botón para deseleccionar todos los archivos MP4 seleccionados
4. LA Interfaz_Web DEBERÁ mostrar las rutas actuales del Directorio_Fuente y Directorio_Destino, cada una limitada a 4096 caracteres
5. LA Interfaz_Web DEBERÁ proporcionar campos de entrada para modificar las rutas del Directorio_Fuente y Directorio_Destino, cada uno aceptando un máximo de 4096 caracteres
6. MIENTRAS los archivos se están convirtiendo, LA Interfaz_Web DEBERÁ mostrar indicadores de progreso para cada Trabajo_Conversion mostrando el porcentaje completado del 0% al 100%
7. SI el Directorio_Fuente está vacío o no contiene archivos MP4, ENTONCES LA Interfaz_Web DEBERÁ mostrar un mensaje indicando que no hay archivos disponibles para conversión
8. SI un usuario ingresa una ruta de directorio inválida, ENTONCES LA Interfaz_Web DEBERÁ mostrar un mensaje de error indicando que la ruta es inválida o inaccesible

### Requisito 2: Descubrimiento y Exploración de Archivos

**Historia de Usuario:** Como usuario, quiero explorar y descubrir archivos MP4 en un directorio específico, para poder seleccionar qué archivos convertir.

#### Criterios de Aceptación

1. CUANDO un usuario proporciona una ruta de Directorio_Fuente, EL Sistema_Conversor DEBERÁ escanear el directorio en busca de archivos MP4 dentro de 5 segundos
2. EL Sistema_Conversor DEBERÁ mostrar una lista de todos los archivos MP4 encontrados en el Directorio_Fuente, mostrando nombre del archivo, tamaño del archivo en bytes y fecha de última modificación en formato ISO 8601
3. CUANDO no se encuentran archivos MP4 en el Directorio_Fuente, LA Interfaz_Web DEBERÁ mostrar un mensaje indicando que no se encontraron archivos MP4 en el directorio especificado
4. SI el Directorio_Fuente no existe o no es accesible, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error indicando que la ruta del directorio es inválida o inaccesible
5. EL Sistema_Conversor DEBERÁ escanear subdirectorios anidados en busca de archivos MP4 cuando el usuario habilita la opción de búsqueda recursiva
6. SI el Directorio_Fuente contiene más de 1000 archivos MP4, ENTONCES EL Sistema_Conversor DEBERÁ mostrar los primeros 1000 archivos e indicar que existen archivos adicionales
7. SI la ruta del Directorio_Fuente excede los 4096 caracteres, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error indicando que la ruta excede la longitud máxima permitida

### Requisito 3: Motor de Conversión de Video

**Historia de Usuario:** Como usuario, quiero que el sistema convierta archivos MP4 a formato AVI, para poder usar los videos en aplicaciones que requieren formato AVI.

#### Criterios de Aceptación

1. CUANDO un usuario inicia la conversión, EL Motor_Conversion DEBERÁ aceptar un máximo de 100 archivos MP4 por lote
2. CUANDO un usuario inicia la conversión, EL Motor_Conversion DEBERÁ convertir cada archivo MP4 seleccionado a formato AVI
3. CUANDO se convierte un archivo MP4, EL Motor_Conversion DEBERÁ preservar la calidad de video tal que el archivo AVI de salida mantenga un bitrate de video de al menos el 90% del original y resolución sin cambios
4. CUANDO se convierte un archivo MP4, EL Motor_Conversion DEBERÁ preservar la calidad de audio tal que el archivo AVI de salida mantenga una tasa de muestreo de audio de al menos el 90% del original y cantidad de canales sin cambios
5. MIENTRAS se convierte un archivo, EL Motor_Conversion DEBERÁ reportar el porcentaje de progreso a la Interfaz_Web en intervalos de 1 segundo o menos
6. CUANDO una conversión se completa exitosamente, EL Sistema_Conversor DEBERÁ guardar el archivo AVI en el Directorio_Destino
7. CUANDO una conversión se completa exitosamente, EL Sistema_Conversor DEBERÁ retener el archivo MP4 original sin modificaciones
8. SI una conversión falla, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error al usuario, registrar el error y continuar con los archivos restantes en el lote
9. EL Motor_Conversion DEBERÁ usar FFmpeg para las operaciones de conversión de video

### Requisito 4: Soporte de Conversión por Lotes

**Historia de Usuario:** Como usuario, quiero convertir múltiples archivos MP4 a la vez, para poder procesar eficientemente grandes bibliotecas de video.

#### Criterios de Aceptación

1. CUANDO un usuario selecciona múltiples archivos MP4 e inicia la conversión, EL Sistema_Conversor DEBERÁ encolar todos los archivos seleccionados para conversión dentro de 2 segundos desde la iniciación
2. EL Sistema_Conversor DEBERÁ procesar los trabajos de conversión secuencialmente para gestionar los recursos del sistema, con un máximo de 1 trabajo convirtiéndose activamente en cualquier momento
3. LA Interfaz_Web DEBERÁ mostrar una cola mostrando conversiones pendientes, en progreso, completadas y fallidas, con cada entrada mostrando el nombre del archivo y el estado actual
4. MIENTRAS la conversión por lotes está en progreso, LA Interfaz_Web DEBERÁ permitir al usuario agregar archivos adicionales a la cola, hasta el límite máximo de lote de 100 archivos
5. CUANDO todas las conversiones en un lote se completan, LA Interfaz_Web DEBERÁ mostrar un resumen mostrando la cantidad de conversiones exitosas y la cantidad de conversiones fallidas
6. EL Sistema_Conversor DEBERÁ soportar un mínimo de 1 archivo y un máximo de 100 archivos por conversión por lote
7. SI el usuario intenta agregar más de 100 archivos a una conversión por lote, ENTONCES LA Interfaz_Web DEBERÁ rechazar los archivos adicionales y mostrar un mensaje de error indicando que se ha alcanzado el límite de 100 archivos

### Requisito 5: Despliegue con Docker

**Historia de Usuario:** Como usuario, quiero desplegar el sistema conversor usando Docker, para poder ejecutarlo fácilmente en cualquier plataforma sin configuración compleja.

#### Criterios de Aceptación

1. EL Sistema_Conversor DEBERÁ estar empaquetado como una imagen Docker
2. CUANDO el contenedor Docker se inicia, EL Sistema_Conversor DEBERÁ estar completamente operativo y accesible dentro de 30 segundos desde la inicialización del contenedor
3. LA imagen Docker DEBERÁ incluir FFmpeg preinstalado y configurado para conversión de video
4. EL contenedor Docker DEBERÁ exponer un puerto configurable para acceso web con un puerto predeterminado de 8000
5. EL contenedor Docker DEBERÁ soportar montaje de volúmenes para acceso al Directorio_Fuente y Directorio_Destino
6. EL Sistema_Conversor DEBERÁ proporcionar un Dockerfile para construir la imagen Docker
7. EL Sistema_Conversor DEBERÁ proporcionar un docker-compose.yml para despliegue simplificado con configuración de volúmenes
8. SI el contenedor Docker falla al iniciar, ENTONCES EL sistema DEBERÁ mostrar un mensaje de error indicando la causa de la falla
9. SI el puerto configurado ya está en uso, ENTONCES EL sistema DEBERÁ mostrar un mensaje de error indicando conflicto de puerto y terminar de manera controlada

### Requisito 6: Configuración de Fuente y Destino

**Historia de Usuario:** Como usuario, quiero configurar directorios fuente y destino, para poder trabajar con archivos en diferentes ubicaciones.

#### Criterios de Aceptación

1. CUANDO la aplicación se inicia, EL Sistema_Conversor DEBERÁ usar rutas configuradas por defecto para Directorio_Fuente y Directorio_Destino
2. CUANDO un usuario envía una nueva ruta de Directorio_Fuente a través de la Interfaz_Web, EL Sistema_Conversor DEBERÁ validar la ruta y actualizar el Directorio_Fuente actual
3. CUANDO un usuario envía una nueva ruta de Directorio_Destino a través de la Interfaz_Web, EL Sistema_Conversor DEBERÁ validar la ruta y actualizar el Directorio_Destino actual
4. CUANDO el Directorio_Fuente se cambia, LA Interfaz_Web DEBERÁ refrescar la lista de archivos dentro de 2 segundos
5. SI el Directorio_Destino no existe, ENTONCES EL Sistema_Conversor DEBERÁ crear la ruta completa del directorio automáticamente
6. SI el usuario no tiene permisos de lectura para el Directorio_Fuente, ENTONCES EL Sistema_Conversor DEBERÁ rechazar el Directorio_Fuente y mostrar un mensaje de error indicando permisos insuficientes
7. SI el usuario no tiene permisos de escritura para el Directorio_Destino, ENTONCES EL Sistema_Conversor DEBERÁ rechazar el Directorio_Destino y mostrar un mensaje de error indicando permisos insuficientes
8. SI un usuario envía una ruta vacía o en blanco para Directorio_Fuente o Directorio_Destino, ENTONCES EL Sistema_Conversor DEBERÁ rechazar la ruta y mostrar un mensaje de error indicando que la ruta no puede estar vacía
9. SI la ruta del Directorio_Fuente no existe, ENTONCES EL Sistema_Conversor DEBERÁ rechazar la ruta y mostrar un mensaje de error indicando que el directorio no fue encontrado

### Requisito 7: Manejo de Errores y Registro

**Historia de Usuario:** Como usuario, quiero mensajes de error claros y registro de eventos, para poder entender y solucionar problemas cuando ocurran.

#### Criterios de Aceptación

1. SI un archivo no puede ser leído, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error con el nombre del archivo y la razón
2. SI una conversión falla, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error con el nombre del archivo, tipo de error y descripción del error
3. SI el Directorio_Destino no tiene permisos de escritura, ENTONCES EL Sistema_Conversor DEBERÁ mostrar un mensaje de error antes de iniciar la conversión
4. MIENTRAS se procesa un lote, EL Sistema_Conversor DEBERÁ continuar con los archivos restantes después de una falla de archivo individual
5. EL Sistema_Conversor DEBERÁ mantener un archivo de registro llamado 'conversion_log.txt' en el Directorio_Destino con entradas con marca de tiempo para todas las operaciones y errores
6. CUANDO una conversión se completa con errores, LA Interfaz_Web DEBERÁ mostrar un resumen conteniendo la cantidad de conversiones fallidas y la lista de nombres de archivos fallidos

### Requisito 8: Seguimiento de Progreso y Estado

**Historia de Usuario:** Como usuario, quiero ver el progreso en tiempo real de las conversiones, para conocer el estado de mis trabajos de conversión.

#### Criterios de Aceptación

1. MIENTRAS una conversión está en progreso, LA Interfaz_Web DEBERÁ mostrar una barra de progreso mostrando el porcentaje de completado del 0% al 100%, actualizando como mínimo cada 1 segundo
2. MIENTRAS una conversión está en progreso, LA Interfaz_Web DEBERÁ mostrar el nombre del archivo actual siendo convertido, truncado a un máximo de 50 caracteres con puntos suspensivos si el nombre excede esta longitud
3. MIENTRAS los archivos están encolados para conversión, LA Interfaz_Web DEBERÁ mostrar la cantidad de archivos restantes en la cola como un número entero no negativo
4. MIENTRAS una conversión está en progreso, LA Interfaz_Web DEBERÁ mostrar el tiempo transcurrido para la conversión actual en formato de horas, minutos y segundos, actualizando cada 1 segundo
5. CUANDO una conversión se completa exitosamente, LA Interfaz_Web DEBERÁ actualizar el estado de conversión para mostrar "Completado" con un indicador visual verde
6. CUANDO una conversión falla, LA Interfaz_Web DEBERÁ actualizar el estado de conversión para mostrar "Fallido" con un indicador visual rojo y un mensaje de error indicando la razón de la falla, limitado a un máximo de 200 caracteres
7. DONDE existan conversiones completadas o fallidas en la visualización de la cola, LA Interfaz_Web DEBERÁ proporcionar un botón para remover estas entradas de la visualización

### Requisito 9: Stack Tecnológico del Frontend

**Historia de Usuario:** Como desarrollador usando este proyecto para aprendizaje, quiero el frontend construido con React y Material-UI, para poder practicar desarrollo frontend moderno para el canal fmoutinhoDev.

#### Criterios de Aceptación

1. LA Interfaz_Web DEBERÁ ser construida usando el framework React
2. LA Interfaz_Web DEBERÁ usar componentes funcionales con hooks
3. LA Interfaz_Web DEBERÁ usar Material-UI (MUI) como librería de componentes para un diseño profesional y moderno
4. CUANDO la Interfaz_Web se renderiza en viewports entre 768 pixeles y 1920 pixeles de ancho, LA Interfaz_Web DEBERÁ mostrar todos los elementos interactivos sin desplazamiento horizontal ni superposición
5. LA Interfaz_Web DEBERÁ usar una arquitectura basada en componentes para mantenibilidad
6. CUANDO la Interfaz_Web se comunica con el backend, LA Interfaz_Web DEBERÁ usar llamadas API RESTful con cuerpos de petición y respuesta JSON
7. LA Interfaz_Web DEBERÁ implementar diseño responsive usando el sistema de grid de Material-UI para adaptarse a diferentes tamaños de pantalla
8. LA Interfaz_Web DEBERÁ usar el sistema de temas de Material-UI para mantener consistencia visual en colores, tipografía y espaciado
9. SI una llamada API RESTful falla debido a error de red o timeout que excede 30 segundos, ENTONCES LA Interfaz_Web DEBERÁ mostrar un mensaje de error indicando la falla y retener cualquier dato ingresado por el usuario

### Requisito 10: API Backend con FastAPI

**Historia de Usuario:** Como desarrollador, quiero una API backend construida con FastAPI para manejar solicitudes de conversión, para que el frontend pueda comunicarse con el motor de conversión aprovechando las ventajas de alto rendimiento, documentación automática y tipado nativo de Python.

#### Criterios de Aceptación

1. EL Sistema_Conversor DEBERÁ proporcionar una API REST para operaciones de exploración de archivos
2. EL Sistema_Conversor DEBERÁ proporcionar un endpoint de API REST para listar archivos MP4 en un directorio
3. EL Sistema_Conversor DEBERÁ proporcionar un endpoint de API REST para iniciar trabajos de conversión y retornar un identificador de trabajo
4. EL Sistema_Conversor DEBERÁ proporcionar un endpoint de API REST para consultar el estado de conversión
5. EL Sistema_Conversor DEBERÁ proporcionar un endpoint de API REST para cancelar un trabajo de conversión
6. EL Sistema_Conversor DEBERÁ proporcionar un endpoint de API REST para actualizar rutas fuente y destino
7. EL Sistema_Conversor DEBERÁ generar documentación automática de la API usando las capacidades integradas de FastAPI (OpenAPI/Swagger)
8. EL Sistema_Conversor DEBERÁ usar tipado nativo de Python con type hints para todos los endpoints y modelos de datos
9. EL Sistema_Conversor DEBERÁ proporcionar validación automática de datos de entrada usando Pydantic
10. SI una petición API falla debido a error del cliente, ENTONCES EL Sistema_Conversor DEBERÁ retornar código de estado HTTP 4xx con mensaje de error indicando la razón de la falla
11. SI una petición API falla debido a error del servidor, ENTONCES EL Sistema_Conversor DEBERÁ retornar código de estado HTTP 5xx con mensaje de error indicando la razón de la falla

### Requisito 11: Arquitectura Hexagonal (Ports & Adapters)

**Historia de Usuario:** Como desarrollador, quiero que el sistema implemente arquitectura hexagonal, para lograr alta testabilidad, mantenibilidad y desacoplamiento entre la lógica de negocio y la infraestructura.

#### Criterios de Aceptación

1. EL Sistema_Conversor DEBERÁ implementar arquitectura hexagonal separando claramente las capas de Dominio, Aplicación e Infraestructura
2. LA Capa_Dominio DEBERÁ contener las entidades de negocio y lógica de dominio pura sin dependencias de infraestructura
3. LA Capa_Aplicacion DEBERÁ contener los casos de uso que orquestan el flujo entre el dominio y la infraestructura
4. LA Capa_Infraestructura DEBERÁ contener los adaptadores para FFmpeg, sistema de archivos, API REST y otros servicios externos
5. EL Sistema_Conversor DEBERÁ definir Puertos como interfaces abstractas que especifican cómo se comunica el dominio con el mundo exterior
6. EL Sistema_Conversor DEBERÁ implementar Adaptadores concretos que conectan los puertos con servicios externos específicos
7. CUANDO se ejecutan pruebas unitarias, EL Sistema_Conversor DEBERÁ permitir sustituir adaptadores de infraestructura por mocks o stubs mediante inyección de dependencias
8. EL Sistema_Conversor DEBERÁ permitir intercambiar componentes de infraestructura sin modificar la lógica de dominio o aplicación
9. DONDE la lógica de negocio depende de servicios externos, EL Sistema_Conversor DEBERÁ depender de abstracciones (Puertos) y no de implementaciones concretas

### Requisito 12: Arquitectura de Microservicio

**Historia de Usuario:** Como desarrollador, quiero que el Sistema_Conversor opere como un microservicio, para permitir despliegue independiente, escalabilidad y mantenimiento aislado.

#### Criterios de Aceptación

1. EL Sistema_Conversor DEBERÁ operar como un servicio independiente con una API bien definida
2. EL Sistema_Conversor DEBERÁ ser stateless, no almacenando estado de sesión entre peticiones
3. EL Sistema_Conversor DEBERÁ ejecutarse en su propio contenedor Docker independiente
4. EL Sistema_Conversor DEBERÁ exponer todos sus servicios a través de la API REST documentada
5. EL Sistema_Conversor DEBERÁ manejar su propia configuración mediante variables de entorno
6. EL Sistema_Conversor DEBERÁ registrar eventos y errores de manera autónoma sin depender de servicios externos de logging
7. SI el Sistema_Conversor necesita comunicarse con otros servicios, ENTONCES DEBERÁ hacerlo exclusivamente a través de su API REST o eventos
