"""
Comanda per crear grups d'usuaris
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from sales_notes.models import Envio


class Command(BaseCommand):
    help = "Crea els grups d'usuaris (DARP, Investigadors, Admin)"

    def handle(self, *args, **kwargs):
        # ContentType per Envio
        envio_ct = ContentType.objects.get_for_model(Envio)

        # Permisos
        view_envio = Permission.objects.get(codename="view_envio", content_type=envio_ct)
        add_envio = Permission.objects.get(codename="add_envio", content_type=envio_ct)

        # Grup DARP
        darp_group, created = Group.objects.get_or_create(name="DARP")
        darp_group.permissions.set([view_envio, add_envio])
        self.stdout.write(self.style.SUCCESS(f'Grup DARP {"creat" if created else "actualitzat"}'))

        # Grup Investigadors
        inv_group, created = Group.objects.get_or_create(name="Investigadors")
        inv_group.permissions.set([view_envio])  # Només lectura
        self.stdout.write(self.style.SUCCESS(f'Grup Investigadors {"creat" if created else "actualitzat"}'))

        self.stdout.write(self.style.SUCCESS("Grups creats correctament!"))
