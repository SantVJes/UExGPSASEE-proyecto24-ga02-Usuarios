from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.usuario_perfiles_inner import UsuarioPerfilesInner
from openapi_server import util

from openapi_server.models.usuario_perfiles_inner import UsuarioPerfilesInner  # noqa: E501

from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, render_template, make_response

db = SQLAlchemy()

def import_db_controller(database):
    global db

# Clase modelo para representar a un usuario en la base de datos.
class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos.

    # Definición de columnas en la tabla `usuarios`.
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único para cada usuario.
    email = db.Column(db.String(255), unique=True, nullable=False)  # Email del usuario (debe ser único y no puede ser nulo).
    password = db.Column(db.String(255), nullable=False)  # Contraseña del usuario (requerida).
    metodo_pago = db.Column(db.String(50), nullable=True)  # Método de pago opcional del usuario.
    status = db.Column(db.Boolean, default=True)  # Estado del usuario (activo por defecto).
    perfiles = db.Column(db.JSON, nullable=True)  # Datos de perfiles asociados al usuario, almacenados en formato JSON.

    # Representación del objeto para depuración.
    def __repr__(self):
        return f'<Usuario {self.email}>'

    # Método para convertir el objeto en un diccionario, útil para convertir el modelo a JSON.
    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "email": self.email,
            "password": self.password,
            "metodo_pago": self.metodo_pago,
            "status": self.status,
            "perfiles": self.perfiles
        }
    
    def verificar_contraseña(self, password):
        return self.password == password  # 

    # Método de clase para crear y guardar un nuevo usuario en la base de datos.
    @classmethod
    def create(cls, email, password, metodo_pago=None, status=True, perfiles=None):
        # Crea una instancia de `Usuario` con los datos proporcionados.
        new_user = cls(
            email=email,
            password=password,
            metodo_pago=metodo_pago,
            status=status,
            perfiles=perfiles
        )

        # Agrega el nuevo usuario a la sesión y guarda los cambios en la base de datos.
        db.session.add(new_user)
        db.session.commit()
        
        # Retorna el objeto creado.
        return new_user
    





'''
class Usuario(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id_usuario=None, email=None, password=None, metodo_pago=None, status=None, perfiles=None):  # noqa: E501
        """Usuario - a model defined in OpenAPI

        :param id_usuario: The id_usuario of this Usuario.  # noqa: E501
        :type id_usuario: int
        :param email: The email of this Usuario.  # noqa: E501
        :type email: str
        :param password: The password of this Usuario.  # noqa: E501
        :type password: str
        :param metodo_pago: The metodo_pago of this Usuario.  # noqa: E501
        :type metodo_pago: str
        :param status: The status of this Usuario.  # noqa: E501
        :type status: str
        :param perfiles: The perfiles of this Usuario.  # noqa: E501
        :type perfiles: List[UsuarioPerfilesInner]
        """
        self.openapi_types = {
            'id_usuario': int,
            'email': str,
            'password': str,
            'metodo_pago': str,
            'status': str,
            'perfiles': List[UsuarioPerfilesInner]
        }

        self.attribute_map = {
            'id_usuario': 'idUsuario',
            'email': 'email',
            'password': 'password',
            'metodo_pago': 'metodoPago',
            'status': 'status',
            'perfiles': 'perfiles'
        }

        self._id_usuario = id_usuario
        self._email = email
        self._password = password
        self._metodo_pago = metodo_pago
        self._status = status
        self._perfiles = perfiles

    @classmethod
    def from_dict(cls, dikt) -> 'Usuario':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Usuario of this Usuario.  # noqa: E501
        :rtype: Usuario
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_usuario(self) -> int:
        """Gets the id_usuario of this Usuario.

        Identificador único del usuario  # noqa: E501

        :return: The id_usuario of this Usuario.
        :rtype: int
        """
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario: int):
        """Sets the id_usuario of this Usuario.

        Identificador único del usuario  # noqa: E501

        :param id_usuario: The id_usuario of this Usuario.
        :type id_usuario: int
        """

        self._id_usuario = id_usuario

    @property
    def email(self) -> str:
        """Gets the email of this Usuario.

        Correo electrónico asociado a la cuenta perteneciente al usuario y junto a la contraseña permiten el acceso a la misma y a los servicios que ofrece la aplicación  # noqa: E501

        :return: The email of this Usuario.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this Usuario.

        Correo electrónico asociado a la cuenta perteneciente al usuario y junto a la contraseña permiten el acceso a la misma y a los servicios que ofrece la aplicación  # noqa: E501

        :param email: The email of this Usuario.
        :type email: str
        """

        self._email = email

    @property
    def password(self) -> str:
        """Gets the password of this Usuario.

        Contraseña que junto al correo electrónico se encuentran asociados a la cuenta perteneciente al usuario y le permiten el acceso a la misma y a los servicios que ofrece la aplicación  # noqa: E501

        :return: The password of this Usuario.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this Usuario.

        Contraseña que junto al correo electrónico se encuentran asociados a la cuenta perteneciente al usuario y le permiten el acceso a la misma y a los servicios que ofrece la aplicación  # noqa: E501

        :param password: The password of this Usuario.
        :type password: str
        """

        self._password = password

    @property
    def metodo_pago(self) -> str:
        """Gets the metodo_pago of this Usuario.

        Forma en la que el usuario realiza el pago correspondiente a los servicios contratados en la aplicación  # noqa: E501

        :return: The metodo_pago of this Usuario.
        :rtype: str
        """
        return self._metodo_pago

    @metodo_pago.setter
    def metodo_pago(self, metodo_pago: str):
        """Sets the metodo_pago of this Usuario.

        Forma en la que el usuario realiza el pago correspondiente a los servicios contratados en la aplicación  # noqa: E501

        :param metodo_pago: The metodo_pago of this Usuario.
        :type metodo_pago: str
        """
        allowed_values = ["tarjeta de credito", "tarjeta virtual", "tarjeta prepago", "paypal"]  # noqa: E501
        if metodo_pago not in allowed_values:
            raise ValueError(
                "Invalid value for `metodo_pago` ({0}), must be one of {1}"
                .format(metodo_pago, allowed_values)
            )

        self._metodo_pago = metodo_pago

    @property
    def status(self) -> str:
        """Gets the status of this Usuario.

        Estado en el que la cuenta asociada al usuario se encuentra en este momento  # noqa: E501

        :return: The status of this Usuario.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Usuario.

        Estado en el que la cuenta asociada al usuario se encuentra en este momento  # noqa: E501

        :param status: The status of this Usuario.
        :type status: str
        """
        allowed_values = ["activo", "en suspension", "pendiente de pago"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def perfiles(self) -> List[UsuarioPerfilesInner]:
        """Gets the perfiles of this Usuario.

        Conjunto de perfiles pertenecientes a la cuenta asociada al usuario. Este atributo se ha definido como un array de objetos, en el cual cada posición almacenará la información referente a un perfil, es decir, nombrePerfil, imagenPerfil y favoritosPerfil  # noqa: E501

        :return: The perfiles of this Usuario.
        :rtype: List[UsuarioPerfilesInner]
        """
        return self._perfiles

    @perfiles.setter
    def perfiles(self, perfiles: List[UsuarioPerfilesInner]):
        """Sets the perfiles of this Usuario.

        Conjunto de perfiles pertenecientes a la cuenta asociada al usuario. Este atributo se ha definido como un array de objetos, en el cual cada posición almacenará la información referente a un perfil, es decir, nombrePerfil, imagenPerfil y favoritosPerfil  # noqa: E501

        :param perfiles: The perfiles of this Usuario.
        :type perfiles: List[UsuarioPerfilesInner]
        """

        self._perfiles = perfiles
'''