"""
Crea usuaris de test per DARP i Investigadors
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Crea usuaris de test (DARP, Investigador)"

    def handle(self, *args, **kwargs):
        # Usuari DARP
        darp_user, created = User.objects.get_or_create(
            username="darp_test",
            defaults={
                "email": "darp@gencat.cat",
                "organization": "DARP_Test - Generalitat de Catalunya",
                "cif_organization": "DARP-TEST-CIF",
                "is_active": True,
            },
        )
        if created:
            darp_user.set_password("DarpPassword123!")
            darp_user.save()
            darp_group = Group.objects.get(name="DARP")
            darp_user.groups.add(darp_group)
            self.stdout.write(self.style.SUCCESS(f"Usuari DARP creat: {darp_user.username}"))
        else:
            self.stdout.write(self.style.WARNING(f"Usuari DARP ja existeix"))

        # Usuari Investigador
        inv_user, created = User.objects.get_or_create(
            username="investigador_test",
            defaults={
                "email": "investigador@icatmar.cat",
                "organization": "ICATMAR_Test - Investigació",
                "cif_organization": "ICATMAR-CIF",
                "is_active": True,
            },
        )
        if created:
            inv_user.set_password("InvPassword123!")
            inv_user.save()
            inv_group = Group.objects.get(name="Investigadors")
            inv_user.groups.add(inv_group)
            self.stdout.write(self.style.SUCCESS(f"Usuari Investigador creat: {inv_user.username}"))
        else:
            self.stdout.write(self.style.WARNING(f"Usuari Investigador ja existeix"))
