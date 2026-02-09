"""
Hashers personalitzats per a compatibilitat amb sistemes legacy.
Implementa algorismes que Django ha eliminat per insegurs (Unsalted MD5/SHA1).
"""

import hashlib

from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.translation import gettext_noop as _


class UnsaltedMD5PasswordHasher(BasePasswordHasher):
    """
    Algorisme MD5 sense salt (insegur, només per compatibilitat legacy).
    """

    algorithm = "unsalted_md5"

    def salt(self):
        return ""

    def encode(self, password, salt):
        assert salt == ""
        return hashlib.md5(password.encode("utf-8")).hexdigest()  # nosec

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, "")
        return encoded == encoded_2

    def safe_summary(self, encoded):
        return {
            _("algorithm"): self.algorithm,
            _("hash"): encoded,
        }


class UnsaltedSHA1PasswordHasher(BasePasswordHasher):
    """
    Algorisme SHA1 sense salt (insegur, només per compatibilitat legacy).
    """

    algorithm = "unsalted_sha1"

    def salt(self):
        return ""

    def encode(self, password, salt):
        assert salt == ""
        return hashlib.sha1(password.encode("utf-8")).hexdigest()  # nosec

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, "")
        return encoded == encoded_2

    def safe_summary(self, encoded):
        return {
            _("algorithm"): self.algorithm,
            _("hash"): encoded,
        }
