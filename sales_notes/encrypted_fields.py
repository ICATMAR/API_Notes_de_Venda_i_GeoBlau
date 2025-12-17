"""
Camps de base de dades xifrats per Django 5.x
Utilitza Fernet (implementació de xifratge simètric AES)
"""

import logging
from decimal import Decimal

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models

logger = logging.getLogger(__name__)


class EncryptionMixin:
    """Mixin per afegir funcionalitat de xifratge a camps Django"""

    @staticmethod
    def get_cipher():
        """Obtenir l'objecte Fernet per xifrar/desxifrar"""
        key = settings.ENCRYPTION_KEY
        if isinstance(key, str):
            key = key.encode()
        return Fernet(key)

    def encrypt_value(self, value):
        """Xifrar un valor"""
        if value is None or value == "":
            return value

        if not isinstance(value, bytes):
            value = str(value).encode("utf-8")

        cipher = self.get_cipher()
        encrypted = cipher.encrypt(value)
        return encrypted.decode("utf-8")

    def decrypt_value(self, value):
        """Desxifrar un valor"""
        if value is None or value == "":
            return value

        try:
            if not isinstance(value, bytes):
                value = value.encode("utf-8")

            cipher = self.get_cipher()
            decrypted = cipher.decrypt(value)
            return decrypted.decode("utf-8")
        except (InvalidToken, Exception) as e:
            logger.error(f"Error desxifrant valor: {e}")
            raise


class EncryptedCharField(EncryptionMixin, models.TextField):
    """
    Camp CharField que xifra automàticament el contingut
    S'emmagatzema com TextField perquè el text xifrat és més llarg
    """

    description = "CharField xifrat amb Fernet"

    def __init__(self, *args, **kwargs):
        # Eliminar max_length ja que TextField no l'accepta
        # Però guardar-lo per possibles validacions futures
        self.original_max_length = kwargs.pop("max_length", None)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Retornar la representació serialitzable del camp"""
        name, path, args, kwargs = super().deconstruct()
        # NO afegir max_length al kwargs per evitar conflictes
        return name, path, args, kwargs

    def get_prep_value(self, value):
        """Xifrar abans de guardar a la BD"""
        if value is None or value == "":
            return value
        return self.encrypt_value(value)

    def from_db_value(self, value, expression, connection):
        """Desxifrar quan es llegeix de la BD"""
        if value is None or value == "":
            return value
        return self.decrypt_value(value)

    def to_python(self, value):
        """Convertir a tipus Python"""
        if isinstance(value, str) or value is None:
            return value
        return str(value)


class EncryptedDecimalField(EncryptionMixin, models.TextField):
    """
    Camp DecimalField que xifra automàticament el contingut
    S'emmagatzema com TextField però manté la validació de Decimal
    """

    description = "DecimalField xifrat amb Fernet"

    def __init__(self, *args, **kwargs):
        # Extreure paràmetres específics de Decimal abans de cridar super()
        self.max_digits = kwargs.pop("max_digits", None)
        self.decimal_places = kwargs.pop("decimal_places", None)

        # Processar validators separadament
        validators = kwargs.get("validators", [])
        if validators:
            # Guardar una còpia dels validators
            self.decimal_validators = list(validators)
        else:
            self.decimal_validators = []

        # Cridar super amb els kwargs nets
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Retornar la representació serialitzable del camp"""
        name, path, args, kwargs = super().deconstruct()
        # NO afegir max_digits ni decimal_places per evitar conflictes
        return name, path, args, kwargs

    def get_prep_value(self, value):
        """Xifrar abans de guardar a la BD"""
        if value is None or value == "":
            return value
        # Convertir Decimal a string abans de xifrar
        value_str = str(value)
        return self.encrypt_value(value_str)

    def from_db_value(self, value, expression, connection):
        """Desxifrar quan es llegeix de la BD"""
        if value is None or value == "":
            return value
        decrypted = self.decrypt_value(value)
        return Decimal(decrypted)

    def to_python(self, value):
        """Convertir a tipus Python (Decimal)"""
        if value is None or value == "":
            return value
        if isinstance(value, Decimal):
            return value
        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return value

    def validate(self, value, model_instance):
        """Validar el valor abans de guardar"""
        super().validate(value, model_instance)
        # Executar validators personalitzats
        if self.decimal_validators:
            for validator in self.decimal_validators:
                validator(value)
