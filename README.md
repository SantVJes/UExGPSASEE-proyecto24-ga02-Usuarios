# Api Usuarios 

## Descripcion 
El **Microservicio de Gestión de Usuarios** es una solución diseñada para manejar de manera eficiente todas las operaciones relacionadas con los usuarios de una plataforma. Su propósito principal es proporcionar un punto centralizado y escalable para gestionar los datos de los usuarios, garantizando la integración fluida con otros microservicios del sistema y el frontend de la aplicación.

### Funcionalidades Principales

- **Gestión Integral de Usuarios**:
  - **Registro**: Permite la creación de nuevos usuarios con validación de datos para asegurar la consistencia de la información.
  - **Consulta**: Facilita la búsqueda de usuarios individuales o el listado completo de usuarios registrados.
  - **Actualización**: Proporciona la capacidad de modificar la información de un usuario existente.
  - **Eliminación**: Soporta la eliminación segura de usuarios, con manejo de datos asociados.

- **Integración con Microservicios**:
  - **Microservicio de Contenidos**: Este microservicio se comunica con la API de contenidos para obtener y gestionar los contenidos favoritos de los usuarios. Esto incluye recomendaciones personalizadas basadas en preferencias individuales.
  - **Microservicio de Vistas**: Proporciona información sobre los contenidos más vistos o interactuados por los usuarios. Esto permite generar estadísticas y adaptar la experiencia del usuario en tiempo real.

- **Interacción con el Frontend**:
  - El microservicio expone una API REST que permite al frontend realizar operaciones de registro, consulta, actualización y eliminación de usuarios.
  - Soporte para flujos de registro y edición en tiempo real mediante validación y retroalimentación.

### Beneficios Clave

- **Eficiencia y Escalabilidad**: Diseñado para manejar grandes volúmenes de usuarios sin afectar el rendimiento.
- **Integración Sólida**: Actúa como un puente entre el frontend y los microservicios relacionados, asegurando la sincronización y consistencia de los datos.
- **Modularidad**: La arquitectura basada en microservicios permite mantener este componente separado, lo que facilita el mantenimiento y la implementación de nuevas funcionalidades.

### Casos de Uso

1. **Registro de un Nuevo Usuario**:
   Un usuario crea una cuenta a través del frontend. La API valida los datos ingresados y almacena la información en la base de datos. Una vez registrado, el microservicio se comunica con otros servicios para configurar sus preferencias iniciales y recomendaciones.

2. **Actualización de Preferencias**:
   Cuando un usuario interactúa con la plataforma, el microservicio recibe información actualizada sobre sus contenidos favoritos desde el servicio de contenidos y vistas, ajustando sus datos en tiempo real.

3. **Eliminación de una Cuenta**:
   Al eliminar un usuario, el microservicio garantiza que toda la información asociada (como preferencias y estadísticas) sea eliminada o archivada según las políticas de privacidad.

4. **Recomendaciones Personalizadas**:
   Utilizando datos proporcionados por el servicio de contenidos, la API actualiza continuamente las recomendaciones del usuario en el frontend, mejorando su experiencia en la plataforma.

---
## 📃 Más Información sobre el Método de Desarrollo

[Infome de la Tercera Entrega](https://github.com/UExGPSASEE/proyecto24-ga02/wiki/🗃%EF%B8%8FInforme-de--Tercera-entrega)

## Requisitos  
Python 3.5.2 o superior  

## Uso  
Para ejecutar el servidor, por favor sigue los siguientes pasos desde el directorio raíz:  

```
pip3 install --no-cache-dir -r requeriments_sqlalchemy.txt
pip3 install -r requirements.txt
python3 -m openapi_server
```

Luego, abre tu navegador y dirígete a la siguiente URL:

```
http://localhost:8080/ui/
```

Tu definición de OpenAPI estará disponible aquí:


