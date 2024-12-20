import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.get_all_perfiles200_response_inner import GetAllPerfiles200ResponseInner  # noqa: E501
from openapi_server.models.usuario import Usuario# noqa: E501
from openapi_server import util
from sqlalchemy.exc import IntegrityError


from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, render_template, make_response

RETUN = "do so magic"
USER = "error: Usuario no encontrado"
db = SQLAlchemy()
def import_db_controller(database):
    global db

def post_iniciar_sesion():
    """Iniciar sesión de usuario en la aplicación

    Verifica las credenciales de un usuario y, si son válidas, inicia sesión.

    :rtype: Union[Dict[str, str], Tuple[Dict[str, str], int]]
    """
    if not request.is_json:
        return jsonify({"error": "La solicitud debe estar en formato JSON"}), 400
    
    data = request.get_json()

    # Extraer y validar campos obligatorios
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Intentar buscar el usuario en la base de datos
    usuario = Usuario.query.filter_by(email=email).first()
    
    # Verificar si el usuario existe y la contraseña es correcta
    if usuario and usuario.verificar_contraseña(password):  #'verificar_contraseña' es un método en Usuario
        # Generar token o mensaje de éxito
        return jsonify({"mensaje": "Inicio de sesión exitoso", "id_usuario": usuario.id_usuario}), 200
    
    
    # Credenciales incorrectas
    return jsonify({"error": "Credenciales incorrectas"}), 401

def add_favorito(id_usuario, nombre_perfil, body):  # noqa: E501
    """Añadir un nuevo contenido al listado de favoritos de un perfil específico de un usuario por su ID

    Añade un nuevo contenido al conjunto de contenidos multimedia favoritos de un perfil específico perteneciente a un usuario en función de su identificador # noqa: E501

    :param id_usuario: ID del usuario al que se le añadirá un contenido a la lista de favoritos de uno de sus perfiles
    :type id_usuario: int
    :param nombre_perfil: nombre del perfil al que se le añadirá un contenido a su lista de favoritos
    :type nombre_perfil: str
    :param body: 
    :type body: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return RETUN



def add_perfil(id_usuario):  # noqa: E501
    """Añadir un nuevo perfil a un usuario por su ID

    Añade un nuevo perfil a un usuario en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario al que se le añadirá un nuevo perfil
    :type id_usuario: int
    :param get_all_perfiles200_response_inner: 
    :type get_all_perfiles200_response_inner: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    try:
        # Convertir el cuerpo JSON recibido en un objeto
        nuevoperfil = connexion.request.get_json()
        
        # Buscar el usuario por ID
        usuario = db.session.query(Usuario).get(id_usuario)
        
        # Verificar si el usuario existe
        if not usuario:
            return USER, 404
        
        # Crear el nuevo perfil sin el nombre
        perfil_sin_nombre = {key: value for key, value in nuevoperfil.items() if key != "nombre_perfil"}
        
        # Verificar si ya existe un perfil con el mismo nombre
        if nuevoperfil["nombre_perfil"] in usuario.perfiles:
            return jsonify({"error": "Ya existe un perfil con este nombre"}), 409
        
        # Crear un diccionario con los perfiles actuales y el nuevo perfil
        perfiles_actualizados = usuario.perfiles.copy()  # Copiar perfiles existentes
        perfiles_actualizados[nuevoperfil["nombre_perfil"]] = perfil_sin_nombre  # Agregar el nuevo perfil
        
        # Actualizar el campo de perfiles con los perfiles combinados
        usuario.perfiles = perfiles_actualizados
        
        # Marcar el usuario como modificado
        db.session.add(usuario)
        db.session.flush()  # Forzar sincronización con la base de datos
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        # Retornar una respuesta con el perfil agregado
        return jsonify({
            "message": "Perfil añadido exitosamente",
            "perfiles": usuario.perfiles
        }), 200

    except KeyError as e:
        # Manejo de errores por clave faltante en el JSON
        return jsonify({"error": f"Falta el campo requerido: {str(e)}"}), 400

    except ValueError as e:
        # Manejo de errores en el valor de los datos proporcionados
        return jsonify({"error": f"Valor inválido en los datos proporcionados: {str(e)}"}), 400

    except Exception as e:
        # Manejo de errores generales
        error_msg = {"error": f"Error al añadir el perfil: {str(e)}"}
        return jsonify(error_msg), 500


def add_usuario():  # noqa: E501
    """Añadir un nuevo usuario a la aplicación

    Crea una nueva cuenta en la aplicación que estará asociada a un nuevo usuario # noqa: E501

    :param usuario: 
    :type usuario: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if request.is_json:
        data = request.get_json()

        # Extraer y validar el objeto 'usuario'
        usuario_data = data.get("usuario")
        if not usuario_data:
            return jsonify({"error": "No ay objeto."}), 400
        
        # Extraer y validar campos obligatorios del usuario
        email = usuario_data.get("email")
        password = usuario_data.get("password")
        metodo_pago = usuario_data.get("metodo_pago")  # Opcional
        status = usuario_data.get("status", True)      # Activo por defecto
        perfiles = usuario_data.get("perfiles")        # Opcional, formato JSON
        if not email or not password:
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        
        try:
        # Crear el nuevo usuario utilizando la función create
            nuevo_usuario = Usuario.create(
                email=email,
                password=password,
                metodo_pago=metodo_pago,
                status=status,
                perfiles=perfiles
              )
            return jsonify({"Usuario Creado"}), 201  # Retorna el nuevo usuario creado

        except IntegrityError:    
            
            return jsonify({"error": "El usuario con ese email ya existe"}), 409  
            
    return jsonify({"error": "La solicitud debe estar en formato JSON"}), 400

     



def delete_perfil(id_usuario, nombre_perfil):  # noqa: E501
    """Eliminar un perfil específico de un usuario por su ID

    Elimina un perfil específico de un usuario registrado en el sistema en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario del que se borrará el perfil
    :type id_usuario: int
    :param nombre_perfil: Nombre del perfil que se borrará
    :type nombre_perfil: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    try:
        # Buscar el usuario por ID
        usuario = db.session.query(Usuario).get(id_usuario)
        
        # Verificar si el usuario existe
        if not usuario:
            return USER, 404

        # Verificar si el perfil a eliminar existe en el usuario
        if nombre_perfil not in usuario.perfiles:
            return jsonify({"error": "Perfil no encontrado"}), 404
        
        # Eliminar el perfil del diccionario de perfiles
        perfiles_actualizados = {k: v for k, v in usuario.perfiles.items() if k != nombre_perfil}

        # Actualizar el campo perfiles con los perfiles actualizados
        usuario.perfiles = perfiles_actualizados

        # Realizar commit para guardar los cambios
        db.session.commit()

        # Retornar respuesta exitosa sin contenido
        return jsonify({"message": "Perfil eliminado exitosamente"}), 204

    except KeyError as e:
        # Manejo de errores por clave faltante
        return jsonify({"error": f"Falta el campo requerido: {str(e)}"}), 400

    except ValueError as e:
        # Manejo de errores en el valor de los datos proporcionados
        return jsonify({"error": f"Valor inválido en los datos proporcionados: {str(e)}"}), 400

    except Exception as e:
        # Manejo de errores generales
        error_msg = {"error": f"Error al eliminar el perfil: {str(e)}"}
        return jsonify(error_msg), 500




def delete_usuario(id_usuario):  # noqa: E501
    """Eliminar un usuario específico por su ID

    Elimina un contenido multimedia específico de la aplicación en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario a borrar
    :type id_usuario: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    try:
        # Obtener el JSON con el email
        datos = request.get_json()
        email = datos.get("email")
        
        if not email:
            return {"error": "El email es requerido"}, 400

        # Buscar el usuario por ID
        usuario = db.session.query(Usuario).get(id_usuario)

        # Verificar si el usuario existe
        if usuario is None:
            return USER, 404

        # Comparar el email recibido con el del usuario a eliminar
        if usuario.email != email:
            return {"error": "El email proporcionado no coincide con el usuario a eliminar"}, 403

        # Eliminar el usuario de la sesión
        db.session.delete(usuario)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Retornar una respuesta de éxito
        return {"message": "Usuario eliminado exitosamente"}, 204

    except Exception as e:
        # Manejo de otros errores
        error_msg = {"error": f"Error al eliminar el usuario: {str(e)}"}
        return error_msg, 500


def get_all_perfiles(id_usuario):  # noqa: E501
    """Obtener una lista de los perfiles asociados a un usuario

    Retorna el conjunto de perfiles asociados a un usuario específico de la aplicación en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario del que se obtendrán sus perfiles
    :type id_usuario: int

    :rtype: Union[List[GetAllPerfiles200ResponseInner], Tuple[List[GetAllPerfiles200ResponseInner], int], Tuple[List[GetAllPerfiles200ResponseInner], int, Dict[str, str]]
    """
    try:
        # Filtrar usuario por ID y obtener sus perfiles
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        
        # Verificar si el usuario existe
        if not usuario:
            return USER, 404
        
        # Verificar si el usuario tiene perfiles
        if not usuario.perfiles:
            return jsonify({"error": "No se encontraron perfiles para este usuario"}), 404
        
        # Devuelve los perfiles en JSON y el código HTTP 200 (OK)
        return jsonify(usuario.perfiles), 200

    except KeyError as e:
        # Manejo de errores por clave faltante
        return jsonify({"error": f"Falta el campo requerido: {str(e)}"}), 400

    except ValueError as e:
        # Manejo de errores en el valor de los datos proporcionados
        return jsonify({"error": f"Valor inválido en los datos proporcionados: {str(e)}"}), 400

    except Exception as e:
        # Manejo de errores generales
        error_msg = {"error": f"Error al obtener perfiles del usuario: {str(e)}"}
        return jsonify(error_msg), 500

    


def get_all_usuarios():  # noqa: E501
    """Obtener la lista de usuarios registrados en la aplicación

    Retorna el conjunto de usuarios registrados en la aplicación # noqa: E501


    :rtype: Union[List[Usuario], Tuple[List[Usuario], int], Tuple[List[Usuario], int, Dict[str, str]]
    """
    
    try:
        # Obtiene todos los registros de usuarios en la base de datos, ordenados por 'status' (activos primero)
        usuarios = Usuario.query.order_by(Usuario.status.desc()).all()  # Ordena por 'status' (True primero, luego False)

        # Convierte cada usuario en un diccionario usando `to_dict`
        usuarios_dict = [usuario.to_dict() for usuario in usuarios]

        return usuarios_dict, 200  # Devuelve la lista de usuarios y el código HTTP 200 (OK)

    except Exception as e:
      # Manejo de errores en caso de fallo en la base de datos u otro problema
        error_msg = {"error": f"Error al obtener usuarios: {str(e)}"}
        return [], 500, error_msg  # Devuelve lista vacía, código 500 y mensaje de error

    
    
    
    return RETUN


def get_favoritos(id_usuario, nombre_perfil):  # noqa: E501
    """Obtener el listado de contenidos multimedia favoritos de un perfil específico de un usuario por su ID

    Retorna el conjunto de contenidos multimedia favoritos de un perfil específico perteneciente a un usuario en función de su identificador # noqa: E501

    :param id_usuario: ID del usuario del que se obtendrá la lista de favoritos de uno de sus perfiles
    :type id_usuario: int
    :param nombre_perfil: nombre del perfil del que se obtendrá su lista de favoritos
    :type nombre_perfil: str

    :rtype: Union[List[int], Tuple[List[int], int], Tuple[List[int], int, Dict[str, str]]
    """
    return RETUN


def get_perfil(id_usuario, nombre_perfil):  # noqa: E501
    """Obtener un perfil específico por su ID

    Retorna los datos de un perfil específico en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario del que se obtendrá el perfil
    :type id_usuario: int
    :param nombre_perfil: Nombre del perfil que se obtendrá
    :type nombre_perfil: str

    :rtype: Union[GetAllPerfiles200ResponseInner, Tuple[GetAllPerfiles200ResponseInner, int], Tuple[GetAllPerfiles200ResponseInner, int, Dict[str, str]]
    """
    try:
        # Filtrar usuario por ID y obtener sus perfiles
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()

        # Verificar si el usuario existe
        if not usuario:
            return USER, 404

        # Verificar si el usuario tiene perfiles y si el perfil especificado existe
        if not usuario.perfiles or nombre_perfil not in usuario.perfiles:
            return jsonify({"error": "Perfil no encontrado para el usuario"}), 404

        # Retornar el perfil específico en función del nombre
        perfil = usuario.perfiles[nombre_perfil]
        return jsonify(perfil), 200  # Devuelve el perfil específico y código HTTP 200 (OK)

    except KeyError as e:
        # Manejo de errores por clave faltante en los datos
        return jsonify({"error": f"Falta el campo requerido: {str(e)}"}), 400

    except ValueError as e:
        # Manejo de errores en el valor de los datos proporcionados
        return jsonify({"error": f"Valor inválido en los datos proporcionados: {str(e)}"}), 400

    except Exception as e:
        # Manejo de errores generales
        error_msg = {"error": f"Error al obtener el perfil: {str(e)}"}
        return jsonify(error_msg), 500  # Devuelve mensaje de error y código HTTP 500


def get_usuario_by_id(id_usuario):  # noqa: E501
    """Obtener un usuario específico por su ID

    Retorna la información de un usuario en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario a devolver
    :type id_usuario: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    return RETUN


def update_perfil(id_usuario, nombre_perfil):  # noqa: E501
    """Actualizar un perfil específico por su ID

    Actualiza un perfil específico de un usuario registrado en el sistema en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario del que se actualizará el perfil
    :type id_usuario: int
    :param nombre_perfil: Nombre del perfil que se actualizará
    :type nombre_perfil: str
    :param get_all_perfiles200_response_inner: 
    :type get_all_perfiles200_response_inner: dict | bytes

    :rtype: Union[GetAllPerfiles200ResponseInner, Tuple[GetAllPerfiles200ResponseInner, int], Tuple[GetAllPerfiles200ResponseInner, int, Dict[str, str]]
    """
    try:
        # Obtener los nuevos datos del perfil desde el cuerpo de la solicitud JSON
        nuevos_datos = connexion.request.get_json()

        # Buscar el usuario por ID
        usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
        
        # Verificar si el usuario existe
        if not usuario:
            return USER, 404

        # Verificar si el perfil especificado existe en los perfiles del usuario
        if not usuario.perfiles or nombre_perfil not in usuario.perfiles:
            return jsonify({"error": "Perfil no encontrado para el usuario"}), 404

        # Crear una copia de los perfiles actuales del usuario
        perfiles_actuales = usuario.perfiles

        # Actualizar solo el perfil específico en la copia
        perfiles_actuales.setdefault(nombre_perfil, {}).update(nuevos_datos)

        # Asignar el diccionario actualizado de perfiles al usuario
        usuario.perfiles = perfiles_actuales

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Retornar una respuesta con el perfil actualizado
        return jsonify({
            "message": "Perfil actualizado exitosamente",
            "perfil_actualizado": usuario.perfiles
        }), 200

    except KeyError as e:
        # Manejo de errores por clave faltante en los datos proporcionados
        return jsonify({"error": f"Falta el campo requerido: {str(e)}"}), 400

    except ValueError as e:
        # Manejo de errores en el valor de los datos proporcionados
        return jsonify({"error": f"Valor inválido en los datos proporcionados: {str(e)}"}), 400

    except Exception as e:
        # Manejo de errores generales
        error_msg = {"error": f"Error al actualizar el perfil: {str(e)}"}
        return jsonify(error_msg), 500



def update_usuario(id_usuario):  # noqa: E501
    """Actualizar un usuario específico por su ID

    Actualiza la información de un usuario registrado en función del identificador proporcionado # noqa: E501

    :param id_usuario: ID del usuario a actualizar
    :type id_usuario: int
    :param usuario: 
    :type usuario: dict | bytes

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        # Obtener los datos JSON del request
        datos_usuario = connexion.request.get_json()

        try:
            # Buscar el usuario en la base de datos por su ID
            usuario_bd = Usuario.query.filter_by(id_usuario=id_usuario).first()# Si no se encuentra, lanza una excepción

            # Actualizar solo los campos que se envían en el JSON
            if 'email' in datos_usuario:
                usuario_bd.email = datos_usuario['email']
            if 'password' in datos_usuario:
                # En caso de que se envíe una nueva contraseña, podría ser un hash en la base de datos
                usuario_bd.password = datos_usuario['password']
            if 'metodo_pago' in datos_usuario:
                usuario_bd.metodo_pago = datos_usuario['metodo_pago']
            if 'status' in datos_usuario:
                usuario_bd.status = datos_usuario['status']
            if 'perfiles' in datos_usuario:
                usuario_bd.perfiles = datos_usuario['perfiles']

            # Confirmar los cambios en la base de datos
            
            db.session.commit()

            # Retornar el usuario actualizado
            return jsonify(usuario_bd.to_dict()), 200  # Puedes usar un método to_dict() si lo tienes en tu modelo

        except Exception as e:
            # Manejo de otros errores genéricos
            return {"error": f"Error al actualizar el usuario: {str(e)}"}, 500


def upload_imagen(id_usuario, nombre_perfil, request_body):  # noqa: E501
    """Actualizar la imagen de un perfil específico de un usuario por su ID

    Actualizar la imagen de un perfil específico perteneciente a un usuario en función de su identificador # noqa: E501

    :param id_usuario: ID del usuario al que se le actualizará la imagen a uno de sus perfiles
    :type id_usuario: int
    :param nombre_perfil: nombre del perfil al que se le actualizará su imagen
    :type nombre_perfil: str
    :param request_body: 
    :type request_body: List[str]

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return RETUN
