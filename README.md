# Proyecto: API REST con Flask, MySQL y Monitorización con Prometheus

## Descripción
Este proyecto consiste en la implementación y despliegue de una API REST basada en Flask, con persistencia de datos en MySQL, utilizando Docker y Docker Compose. Además, se incorpora monitorización con Prometheus y Grafana para supervisar el rendimiento de los servicios.

## Objetivos de Aprendizaje
- Creación de servicios disponibles vía API REST.
- Soluciones basadas en contenedores.
- Orquestación de contenedores con Docker Compose.
- Monitorización del rendimiento de servicios.
- Servicios escalables y despliegue en la nube.

## Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Base de datos**: MySQL
- **Gestor de BD**: Adminer
- **Contenedores**: Docker, Docker Compose
- **Monitorización**: Prometheus, Grafana, mysqld-exporter

## Arquitectura
El proyecto se compone de los siguientes contenedores:
1. **Base de datos (MySQL)**: Almacena los mensajes.
2. **Adminer**: Interfaz web para gestionar MySQL.
3. **API REST (Flask)**: Exposición de endpoints para CRUD de mensajes.
4. **Prometheus**: Recoge métricas de Flask y MySQL.
5. **Grafana**: Visualización de métricas.
6. **mysqld-exporter**: Traduce métricas de MySQL para Prometheus.

## Endpoints de la API REST
- `GET /` → Mensaje de prueba
- `GET /data` → Obtener todos los registros
- `GET /data/<int:clid>` → Obtener un registro por ID
- `POST /data` → Insertar un nuevo registro
- `PUT /data/<int:clid>` → Actualizar un registro existente
- `DELETE /data/<int:clid>` → Eliminar un registro

## Despliegue con Docker Compose
### **Requisitos previos**
- Tener instalados **Docker** y **Docker Compose**.

### **Pasos de despliegue**
1. Clonar el repositorio:
   ```sh
   git clone https://github.com/inigovilaa/docker-proyecto1.git
   cd docker-proyecto1
   ```
2. Construir y levantar los contenedores:
   ```sh
   docker-compose up --build -d
   ```
3. Acceder a los servicios:
   - API REST: `http://localhost:4000`
   - Adminer: `http://localhost:8080`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000`
   
## Monitorización con Prometheus y Grafana
- La API REST expone métricas en `http://localhost:4000/metrics`.
- mysqld-exporter expone métricas de MySQL en `http://localhost:9104/metrics`.
- Grafana permite visualizar las métricas mediante dashboards preconfigurados.

## Autores
Este proyecto fue realizado por **Jiayuan Wang** e **Iñigo Vilá** para la asignatura de Infraestructuras para el Procesamiento Masivo de Datos.


