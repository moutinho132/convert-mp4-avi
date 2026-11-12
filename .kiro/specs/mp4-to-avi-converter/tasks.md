# Implementation Plan: Sistema Conversor de MP4 a AVI

## Overview

Este documento describe el plan de implementación incremental del Sistema Conversor de MP4 a AVI. El sistema implementa una arquitectura hexagonal con Python/FastAPI en el backend, React con Material-UI en el frontend, y FFmpeg como motor de conversión, todo desplegado mediante contenedores Docker.

## Tasks

- [ ] 1. Configurar estructura del proyecto y dependencias
  - Crear estructura de directorios para backend (arquitectura hexagonal)
  - Crear estructura de directorios para frontend React
  - Configurar archivos de dependencias (requirements.txt, package.json)
  - Configurar herramientas de desarrollo (pytest, ESLint, Prettier)
  - _Requisitos: 11.1, 11.2, 11.3_

- [ ] 2. Implementar capa de dominio del backend
  - [ ] 2.1 Crear entidades de dominio (FileEntity, ConversionJob, FileJob)
    - Implementar FileEntity con validaciones
    - Implementar ConversionJob con lógica de estado
    - Implementar value objects (FilePath, ConversionOptions)
    - _Requisitos: 11.2_

  - [ ] 2.2 Definir puertos (interfaces abstractas)
    - Implementar IFileRepository
    - Implementar IConversionService
    - Implementar IFileSystemService
    - _Requisitos: 11.5_

  - [ ] 2.3 Implementar excepciones de dominio
    - Crear jerarquía de excepciones (DomainException, PathTooLongError, etc.)
    - _Requisitos: 7.1, 7.2_

- [ ] 3. Implementar capa de aplicación del backend
  - [ ] 3.1 Crear DTOs con Pydantic
    - Implementar FileRequestDTO, FileResponseDTO, FileListResponseDTO
    - Implementar ConversionRequestDTO, ConversionStatusResponseDTO
    - Implementar ConfigRequestDTO, ConfigResponseDTO
    - _Requisitos: 10.8, 10.9_

  - [ ] 3.2 Implementar caso de uso ListFilesUseCase
    - Escanear directorio y retornar lista de archivos MP4
    - Validar longitud de ruta y permisos
    - Limitar resultados a 1000 archivos
    - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [ ] 3.3 Implementar caso de uso ConvertVideoUseCase
    - Crear trabajo de conversión
    - Validar ruta destino
    - Procesar archivos secuencialmente
    - Broadcast de progreso via WebSocket
    - _Requisitos: 3.1, 3.2, 4.1, 4.2_

  - [ ] 3.4 Implementar caso de uso GetConversionStatusUseCase
    - Consultar estado de trabajo
    - Calcular tiempo transcurrido
    - Retornar progreso detallado
    - _Requisitos: 8.1, 8.2, 8.3, 8.4_

  - [ ] 3.5 Implementar caso de uso CancelConversionUseCase
    - Cancelar trabajo en progreso
    - Actualizar estado del trabajo
    - _Requisitos: 10.5_

  - [ ] 3.6 Implementar caso de uso SetConfigUseCase
    - Validar y actualizar rutas de configuración
    - Verificar permisos de lectura/escritura
    - _Requisitos: 6.1, 6.2, 6.3, 6.5, 6.6, 6.7, 6.8, 6.9_

- [ ] 4. Implementar capa de infraestructura del backend
  - [ ] 4.1 Crear adaptador FFmpegAdapter
    - Implementar conversión MP4 a AVI
    - Parsear progreso desde stderr de FFmpeg
    - Manejar errores de conversión
    - Obtener versión de FFmpeg
    - _Requisitos: 3.2, 3.3, 3.4, 3.5, 3.9_

  - [ ] 4.2 Crear adaptador FileSystemAdapter
    - Implementar escaneo de directorios
    - Validar rutas fuente y destino
    - Verificar permisos de lectura/escritura
    - Crear directorios si no existen
    - _Requisitos: 2.1, 2.4, 6.4, 6.5, 6.6, 6.7_

  - [ ] 4.3 Crear adaptador InMemoryRepository
    - Implementar almacenamiento en memoria de trabajos
    - Operaciones CRUD para ConversionJob
    - _Requisitos: 11.6_

  - [ ] 4.4 Implementar WebSocketManager
    - Gestión de conexiones activas
    - Broadcast de mensajes de progreso
    - Manejo de desconexiones
    - _Requisitos: 8.1, 8.5, 8.6_

  - [ ] 4.5 Implementar sistema de logging
    - Crear ConversionLogger
    - Escribir conversion_log.txt en Directorio_Destino
    - Formato con timestamp ISO 8601
    - _Requisitos: 7.5_

- [ ] 5. Implementar capa de API REST (FastAPI)
  - [ ] 5.1 Configurar aplicación FastAPI principal
    - Crear main.py con lifespan management
    - Configurar CORS middleware
    - Configurar inyección de dependencias
    - _Requisitos: 10.1, 10.7_

  - [ ] 5.2 Implementar router de archivos (/api/files)
    - Endpoint GET /api/files para listar MP4
    - Validación de parámetros
    - Manejo de errores HTTP
    - _Requisitos: 10.2, 10.10, 10.11_

  - [ ] 5.3 Implementar router de conversión (/api/convert)
    - Endpoint POST /api/convert para iniciar conversión
    - Endpoint GET /api/convert/{job_id}/status
    - Endpoint DELETE /api/convert/{job_id} para cancelar
    - WebSocket /api/ws/conversion/{job_id}
    - _Requisitos: 10.3, 10.4, 10.5_

  - [ ] 5.4 Implementar router de configuración (/api/config)
    - Endpoint PUT /api/config/paths
    - Validación de rutas
    - _Requisitos: 10.6_

  - [ ] 5.5 Implementar router de health check
    - Endpoint GET /health
    - Verificar disponibilidad de FFmpeg
    - Retornar estado del servicio
    - _Requisitos: 5.2, 5.8_

  - [ ] 5.6 Implementar middleware de manejo de errores
    - Capturar excepciones de dominio
    - Mapear a códigos HTTP apropiados
    - Formato consistente de respuestas de error
    - _Requisitos: 7.1, 7.2, 7.3, 10.10, 10.11_

- [ ] 6. Punto de control - Verificar backend
  - Ejecutar tests unitarios del dominio
  - Ejecutar tests de integración de API
  - Verificar documentación OpenAPI en /docs
  - Asegurar que todos los tests pasan

- [ ] 7. Implementar estructura del frontend React
  - [ ] 7.1 Configurar proyecto React con TypeScript
    - Inicializar proyecto con Vite
    - Configurar TypeScript
    - Instalar dependencias (React, MUI, react-router)
    - _Requisitos: 9.1, 9.2_

  - [ ] 7.2 Configurar tema Material-UI
    - Crear theme.ts con paleta personalizada
    - Configurar ThemeProvider
    - Aplicar CssBaseline
    - _Requisitos: 9.8_

  - [ ] 7.3 Crear tipos TypeScript
    - Definir interfaces para File, ConversionJob, Config
    - _Requisitos: 9.6_

- [ ] 8. Implementar contexto y hooks de estado
  - [ ] 8.1 Crear AppContext para estado global
    - Estado de archivos seleccionados
    - Estado de trabajos de conversión
    - Estado de configuración de rutas
    - _Requisitos: 1.2, 1.3_

  - [ ] 8.2 Implementar hook useFiles
    - Obtener lista de archivos del backend
    - Manejar loading y errores
    - Refrescar lista
    - _Requisitos: 1.1, 2.1, 2.2_

  - [ ] 8.3 Implementar hook useConversion
    - Iniciar conversión via API
    - Consultar estado de trabajos
    - Cancelar conversión
    - _Requisitos: 4.1, 4.3_

  - [ ] 8.4 Implementar hook useWebSocket
    - Conectar a WebSocket del backend
    - Recibir actualizaciones de progreso
    - Manejar reconexión
    - _Requisitos: 8.1_

  - [ ] 8.5 Implementar hook useConfig
    - Actualizar rutas de configuración
    - Validar rutas antes de enviar
    - _Requisitos: 6.2, 6.3_

- [ ] 9. Implementar componentes de UI con Material-UI
  - [ ] 9.1 Crear componente AppLayout
    - Layout principal responsive
    - AppBar con título
    - _Requisitos: 9.4, 9.7_

  - [ ] 9.2 Crear componente FileBrowser
    - Lista de archivos MP4 con MUI List
    - Checkbox para selección individual
    - Botones seleccionar/deseleccionar todos
    - Opción de búsqueda recursiva
    - Mostrar nombre, tamaño, fecha
    - _Requisitos: 1.1, 1.2, 1.3, 1.7, 2.2, 2.6_

  - [ ] 9.3 Crear componente ConversionQueue
    - Mostrar cola de conversiones
    - Estados: pendiente, en progreso, completado, fallido
    - Botón para iniciar conversión
    - Botón para limpiar completados
    - Chips de estado con MUI
    - _Requisitos: 4.3, 4.5, 8.5, 8.6_

  - [ ] 9.4 Crear componente ProgressTracker
    - Barra de progreso MUI LinearProgress
    - Archivo actual siendo convertido
    - Tiempo transcurrido
    - Archivos restantes
    - Contadores de completados/fallidos
    - _Requisitos: 1.6, 8.1, 8.2, 8.3, 8.4_

  - [ ] 9.5 Crear componente PathConfig
    - Campos de texto para rutas con MUI TextField
    - Botón guardar cambios
    - Validación de rutas vacías
    - _Requisitos: 1.4, 1.5, 1.8, 6.1, 6.2, 6.3_

  - [ ] 9.6 Crear componentes comunes
    - LoadingSpinner con MUI CircularProgress
    - ErrorMessage con MUI Alert
    - EmptyState para listas vacías
    - _Requisitos: 9.7_

- [ ] 10. Integrar frontend con backend
  - [ ] 10.1 Configurar servicio API
    - Cliente HTTP con fetch
    - Manejo de errores de red
    - Timeout de 30 segundos
    - _Requisitos: 9.6, 9.9_

  - [ ] 10.2 Conectar FileBrowser con API
    - Cargar archivos al montar componente
    - Actualizar al cambiar directorio fuente
    - _Requisitos: 1.1, 6.4_

  - [ ] 10.3 Conectar ConversionQueue con WebSocket
    - Recibir actualizaciones de progreso en tiempo real
    - Actualizar estado de trabajos
    - Mostrar resumen al completar
    - _Requisitos: 4.5, 8.1, 8.5, 8.6_

  - [ ] 10.4 Conectar PathConfig con API
    - Validar y guardar rutas
    - Mostrar errores de validación
    - Refrescar lista de archivos al cambiar ruta
    - _Requisitos: 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_

- [ ] 11. Punto de control - Verificar frontend
  - Verificar diseño responsive (768px - 1920px)
  - Verificar comunicación con backend
  - Verificar actualizaciones WebSocket
  - Asegurar que no hay errores en consola

- [ ] 12. Implementar tests del backend
  - [ ]* 12.1 Escribir tests unitarios del dominio
    - Tests para FileEntity
    - Tests para ConversionJob
    - Tests para validaciones
    - _Requisitos: 11.7_

  - [ ]* 12.2 Escribir tests unitarios de casos de uso
    - Tests para ListFilesUseCase
    - Tests para ConvertVideoUseCase
    - Tests para GetConversionStatusUseCase
    - Usar mocks para adaptadores
    - _Requisitos: 11.7_

  - [ ]* 12.3 Escribir tests de integración de API
    - Tests para endpoints REST
    - Tests para WebSocket
    - Tests de manejo de errores
    - _Requisitos: 10.10, 10.11_

- [ ] 13. Implementar tests del frontend
  - [ ]* 13.1 Escribir tests de componentes React
    - Tests para FileBrowser
    - Tests para ConversionQueue
    - Tests para ProgressTracker
    - Tests para PathConfig
    - _Requisitos: 9.4_

  - [ ]* 13.2 Escribir tests de integración frontend
    - Tests de flujo completo de conversión
    - Tests de manejo de errores
    - _Requisitos: 1.8, 9.9_

- [ ] 14. Configurar Docker y despliegue
  - [ ] 14.1 Crear Dockerfile multi-stage
    - Stage 1: Build frontend React
    - Stage 2: Imagen Python con FFmpeg
    - Copiar build de frontend a estáticos
    - Usuario no-root
    - _Requisitos: 5.1, 5.3_

  - [ ] 14.2 Crear docker-compose.yml
    - Configurar volúmenes para source y output
    - Configurar puerto (8000)
    - Variables de entorno
    - Healthcheck
    - Límites de recursos
    - _Requisitos: 5.4, 5.5, 5.6, 5.7_

  - [ ] 14.3 Crear archivo .env.example
    - Documentar todas las variables de entorno
    - Valores por defecto
    - _Requisitos: 12.5_

  - [ ] 14.4 Verificar inicio del contenedor
    - Container startup en menos de 30 segundos
    - Health check funcional
    - Manejo de errores de puerto en uso
    - _Requisitos: 5.2, 5.8, 5.9_

- [ ] 15. Punto de control final - Verificar sistema completo
  - Ejecutar todos los tests
  - Verificar build de Docker
  - Verificar despliegue con docker-compose
  - Verificar documentación API en /docs
  - Probar flujo completo de conversión

## Notes

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requisitos específicos para trazabilidad
- Los puntos de control aseguran validación incremental
- La arquitectura hexagonal permite testing aislado del dominio
- El sistema no es adecuado para property-based testing debido a dependencias de I/O externo

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "2.2", "2.3"] },
    { "id": 2, "tasks": ["3.1"] },
    { "id": 3, "tasks": ["3.2", "3.3", "3.4", "3.5", "3.6"] },
    { "id": 4, "tasks": ["4.1", "4.2", "4.3", "4.4", "4.5"] },
    { "id": 5, "tasks": ["5.1"] },
    { "id": 6, "tasks": ["5.2", "5.3", "5.4", "5.5", "5.6"] },
    { "id": 7, "tasks": ["7.1", "7.2", "7.3"] },
    { "id": 8, "tasks": ["8.1", "8.2", "8.3", "8.4", "8.5"] },
    { "id": 9, "tasks": ["9.1"] },
    { "id": 10, "tasks": ["9.2", "9.3", "9.4", "9.5", "9.6"] },
    { "id": 11, "tasks": ["10.1"] },
    { "id": 12, "tasks": ["10.2", "10.3", "10.4"] },
    { "id": 13, "tasks": ["12.1", "12.2", "12.3", "13.1", "13.2"] },
    { "id": 14, "tasks": ["14.1", "14.2", "14.3"] },
    { "id": 15, "tasks": ["14.4"] }
  ]
}
```
