"""
Permisos personalitzats per a notes de venda
"""

from rest_framework import permissions


class IsDARP(permissions.BasePermission):
    """
    Permís per usuaris DARP (Generalitat Catalunya)

    DARP pot:
    - Crear enviaments (POST)
    - Consultar els seus propis enviaments (GET)
    """

    def has_permission(self, request, view):
        """Verificar si l'usuari pertany a DARP"""
        if not request.user or not request.user.is_authenticated:
            return False

        # Comprovar si l'usuari té el permís per afegir enviaments
        return request.user.has_perm("sales_notes.add_envio")


class IsInvestigador(permissions.BasePermission):
    """
    Permís per investigadors

    Investigadors poden:
    - Consultar TOTES les notes de venda (GET) - només lectura
    - NO poden crear ni modificar
    """

    def has_permission(self, request, view):
        """Verificar si l'usuari és investigador"""
        if not request.user or not request.user.is_authenticated:
            return False

        # Comprovar si l'usuari pertany al grup 'Investigadors'
        # o si té un camp específic
        return request.user.groups.filter(name="Investigadors").exists()


class DARPCanCreateInvestigadorCanRead(permissions.BasePermission):
    """
    Permís combinat:
    - DARP: Pot crear (POST) i llegir els seus enviaments (GET)
    - Investigadors: Només poden llegir TOTS els enviaments (GET)
    - Admin: Control total
    """

    def has_permission(self, request, view):
        """Verificar permís a nivell de vista"""
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin pot fer-ho tot
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Investigadors només GET (safe methods)
        if request.user.groups.filter(name="Investigadors").exists():
            return request.method in permissions.SAFE_METHODS  # GET, HEAD, OPTIONS

        # Qualsevol usuari amb permís per afegir pot fer POST i GET
        if request.user.has_perm("sales_notes.add_envio"):
            return request.method in ["GET", "POST", "HEAD", "OPTIONS"]

        # Per defecte, denegar
        return False

    def has_object_permission(self, request, view, obj):
        """Verificar permís a nivell d'objecte (enviament específic)"""
        # Admin pot veure tot
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Investigadors poden veure tot (només lectura)
        if request.user.groups.filter(name="Investigadors").exists():
            return request.method in permissions.SAFE_METHODS

        # Els usuaris amb permís per afegir només poden veure els seus propis enviaments
        if request.user.has_perm("sales_notes.add_envio"):
            # Només els enviaments creats per aquest usuari
            return obj.usuario_envio == request.user

        return False
