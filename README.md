# Registro de Infracciones de Tránsito

Este proyecto es un sistema de registro de infracciones de tránsito desarrollado en Django. Incluye una interfaz administrativa y APIs para registrar y consultar infracciones, utiliza Docker para la contenedorización, Nginx como proxy inverso y JWT para la autenticación.

## Características

1. **Interfaz Administrativa**:
   - Permite gestionar registros de Personas, Vehículos y Oficiales.
   - Crear, ver, modificar y borrar registros garantizando la integridad referencial.

2. **API para Cargar Infracciones**:
   - Método `cargar_infraccion` que recibe datos de una infracción en formato JSON.
   - Autenticación mediante Bearer Token (JWT).

3. **API para Generar Informe**:
   - Método `generar_informe` que devuelve un listado de infracciones asociadas a una persona según su correo electrónico.

## Tecnologías Utilizadas

- **Django**: Framework web utilizado para desarrollar la aplicación.
- **Django REST Framework**: Para construir la API.
- **Django REST Framework SimpleJWT**: Para la autenticación mediante JWT.
- **Nginx**: Usado como proxy inverso para servir la aplicación.
- **Docker**: Para la contenedorización de la aplicación.
- **PostgreSQL**: Base de datos utilizada para almacenar los registros.

## Instalación y Configuración

### Requisitos

- Docker y Docker Compose
- Python 3.8 o superior

## Uso sin Docker

### Pasos

1. **Clonar el Repositorio**

   ```sh
   git clone https://github.com/tuusuario/registro_infracciones_transito.git
   cd registro_infracciones_transito
   ```

2. **Crear un Entorno Virtual**

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usar `venv\Scripts\activate`
   ```

3. **Instalar Dependencias**

   ```sh
   pip install -r requirements.txt
   ```

4. **Ejecutar Migraciones**

   ```sh
   python manage.py migrate
   ```

5. **Crear Superusuario**

   ```sh
   python manage.py createsuperuser
   ```

6. **Ejecutar el Servidor**

   ```sh
   python manage.py runserver
   ```

   Accede a la interfaz administrativa en `http://127.0.0.1:8000/admin`.

## Uso con Docker

### Ambiente de Desarrollo

1. **Construir y Ejecutar los Contenedores**

   ```sh
   docker-compose -f docker-compose.yml up -d --build
   ```

2. **Acceder a la Aplicación**

   - Interfaz Administrativa: `http://127.0.0.1:8000/admin`

   Por defecto, se crea el superusuario `admin` con contraseña `admin`.

### Configuraciones de los Contenedores

- Las configuraciones de los contenedores se encuentran en `docker-compose.yml` y en los archivos dentro del directorio `compose/dev`.
- En `compose/dev` hay dos directorios:
  - `postgres`: Contiene las configuraciones referentes al gestor de base de datos.
  - `django`: Contiene las configuraciones de Django.

### Ambiente de Producción

1. **Construir y Ejecutar los Contenedores**

   ```sh
   docker-compose -f docker-compose-prod.yml up -d --build
   ```

   Esto agregará un contenedor Nginx que actúa como proxy inverso, mientras que Gunicorn maneja las solicitudes de los clientes y sirve archivos estáticos.

2. **Acceder a la Aplicación**

   - Interfaz Administrativa: `http://127.0.0.1:8000/admin`

### Configuraciones de los Contenedores

- Las configuraciones de los contenedores de producción se encuentran en `compose/prod`.

## Detener los Contenedores

Para detener los contenedores, utiliza los siguientes comandos dependiendo del ambiente que estés ejecutando:

- Ambiente de Desarrollo:

  ```sh
  docker-compose -f docker-compose.yml down -v
  ```

- Ambiente de Producción:

  ```sh
  docker-compose -f docker-compose-prod.yml down -v
  ```

## Uso de la API

### Documentación de la API

La API está documentada con Swagger y ReDoc. Para acceder a ellas:

- Si estás utilizando la opción sin Docker o el Docker de desarrollo, puedes acceder mediante las URLs:
  - Swagger: `http://127.0.0.1:8000/swagger/`
  - ReDoc: `http://127.0.0.1:8000/redoc/`

- Si estás ejecutando Docker para producción, puedes hacerlo mediante las URLs:
  - Swagger: `http://127.0.0.1/swagger/`
  - ReDoc: `http://127.0.0.1/redoc/`

### Obtener un Token JWT

Para obtener un token JWT, realiza una solicitud POST a `/api/token/` con el nombre de usuario y la contraseña del usuario.

```sh
curl -X POST http://localhost/api/token/ -d "username=admin&password=adminpassword"
```

### Cargar una Infracción

Envía una solicitud POST a `/api/cargar_infraccion/` con los detalles de la infracción y el token JWT en el encabezado.

```sh
curl -X POST http://localhost/api/cargar_infraccion/ -H "Authorization: Bearer <your_token>" -d '{
    "placa_patente": "ABC123",
    "timestamp": "2024-06-06T15:06:08Z",
    "comentarios": "Ejemplo de infracción"
}'
```

### Generar un Informe

Envía una solicitud GET a `/api/generar_informe/?email=correo@example.com` para obtener el listado de infracciones asociadas a la persona con ese correo electrónico.

```sh
curl -X GET http://localhost/api/generar_informe/?email=correo@example.com
```

## Arquitectura de Servicios en AWS

Para desplegar esta aplicación en AWS, se recomienda utilizar los siguientes servicios:

- **Amazon ECS (Elastic Container Service)**: Para ejecutar los contenedores Docker.
- **Amazon RDS (Relational Database Service)**: Para alojar la base de datos PostgreSQL.
- **Amazon S3 (Simple Storage Service)**: Para almacenar archivos estáticos y de medios.
- **Amazon CloudFront**: Para la distribución de contenido estático y mejorar el rendimiento.
- **Amazon ALB (Application Load Balancer)**: Para distribuir el tráfico entre los contenedores de ECS.