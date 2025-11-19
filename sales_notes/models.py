"""
Models per a la gestió de Notes de Venda (VCPE)
Basat en l'esquema JSON proporcionat pel Ministeri
"""

import uuid
from decimal import Decimal

from django.contrib.gis.db import models
from django.core.validators import  MinValueValidator,RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from .existing_models import Port, Species, Vessel


class TimeStampedModel(models.Model):
    """Model abstracte amb timestamps per auditoria"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Envio(TimeStampedModel):
    """
    Model principal que representa un enviament de notes de venda
    Correspon a l'arrel de l'esquema JSON
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_envio = models.CharField(max_length=50, unique=True, db_index=True, help_text="Número únic d'enviament")

    TIPO_RESPUESTA_CHOICES = [
        (1, "Completa"),
        (2, "Media"),
        (3, "Reducida"),
    ]
    tipo_respuesta = models.IntegerField(
        choices=TIPO_RESPUESTA_CHOICES, default=1, help_text="Tipus de resposta esperada del sistema"
    )

    # Metadades de processament
    fecha_recepcion = models.DateTimeField(default=timezone.now, db_index=True)
    procesado = models.BooleanField(default=False, db_index=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)

    # Validació i errors
    validado = models.BooleanField(default=False)
    errores = models.JSONField(default=list, blank=True)

    # IP i usuari per auditoria
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    usuario_envio = models.ForeignKey("authentication.APIUser", on_delete=models.PROTECT, related_name="envios")

    class Meta:
        db_table = "envio"
        ordering = ["-fecha_recepcion"]
        verbose_name = "Enviament"
        verbose_name_plural = "Enviaments"
        indexes = [
            models.Index(fields=["num_envio", "fecha_recepcion"]),
            models.Index(fields=["procesado", "validado"]),
        ]

    def __str__(self):
        return f"Envio {self.num_envio} - {self.fecha_recepcion}"


class EstablecimientoVenta(TimeStampedModel):
    """
    Establiment de venda (llotja, punt de venda)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="establecimientos")

    num_identificacion_establec = models.CharField(
        max_length=50, db_index=True, help_text="Número d'identificació de l'establiment"
    )

    class Meta:
        db_table = "establecimiento_venta"
        ordering = ["num_identificacion_establec"]
        verbose_name = "Establiment de venda"
        verbose_name_plural = "Establiments de venda"
        unique_together = [["envio", "num_identificacion_establec"]]

    def __str__(self):
        return f"Establiment {self.num_identificacion_establec}"


class UnidadProductiva(TimeStampedModel):
    """
    Model abstracte per unitats productives (Buque, Granja, PersonaFisJur)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    establecimiento = models.ForeignKey(
        EstablecimientoVenta, on_delete=models.CASCADE, related_name="unidades_productivas"
    )

    METODO_PRODUCCION_CHOICES = [
        (1, "Pesca extractiva marina"),
        (2, "Aqüicultura marina"),
        (3, "Pesca extractiva aigües interiors"),
        (4, "Aqüicultura aigües interiors"),
    ]
    metodo_produccion = models.IntegerField(choices=METODO_PRODUCCION_CHOICES, db_index=True)

    # Discriminador per saber quin tipus d'unitat és
    tipo_unidad = models.CharField(
        max_length=20,
        choices=[
            ("BUQUE", "Vaixell"),
            ("GRANJA", "Granja"),
            ("PERSONA", "Persona Física/Jurídica"),
        ],
        db_index=True,
    )

    class Meta:
        db_table = "unidad_productiva"
        ordering = ["created_at"]
        verbose_name = "Unitat productiva"
        verbose_name_plural = "Unitats productives"
        indexes = [
            models.Index(fields=["tipo_unidad", "metodo_produccion"]),
        ]

    def __str__(self):
        return f"{self.get_tipo_unidad_display()} - Mètode {self.metodo_produccion}"


class Buque(models.Model):
    """
    Dades específiques per vaixells pesquers
    """

    unidad_productiva = models.OneToOneField(
        UnidadProductiva, on_delete=models.CASCADE, primary_key=True, related_name="buque"
    )

    codigo_buque = models.CharField(max_length=20, db_index=True, help_text="Codi del vaixell (matrícula)")

    vessel_ref = models.ForeignKey(
        Vessel,
        on_delete=models.PROTECT,
        to_field="code",
        related_name="ventas_buque",
        null=True,
        blank=True,
        help_text="Referència al vaixell del catàleg",
    )

    puerto_al5_validator = RegexValidator(
        regex=r"^[A-Za-z]{2}[A-Za-z0-9]{3}$", message="Format invàlid. Ha de ser 2 lletres + 3 alfanumèrics (ex: ESBAR)"
    )
    puerto_al5 = models.CharField(
        max_length=5, validators=[puerto_al5_validator], blank=True, null=True, help_text="Codi del port en format AL5"
    )

    port_ref = models.ForeignKey(
        Port,
        on_delete=models.PROTECT,
        related_name="ventas_puerto",
        null=True,
        blank=True,
        help_text="Referència al port del catàleg",
    )

    armador = models.CharField(max_length=100, blank=True, null=True)
    capitan = models.CharField(max_length=60, blank=True, null=True)

    fecha_regreso_puerto = models.DateTimeField(help_text="Data i hora de retorn al port")

    cod_marea = models.CharField(max_length=50, blank=True, null=True, help_text="Codi de marea")

    def clean(self):
        """Validar i sincronitzar vaixell i port amb catàleg"""

        errors = {}

        # Validar vaixell
        if self.codigo_buque:
            try:
                vessel = Vessel.objects.get(code=self.codigo_buque)
                self.vessel_ref = vessel
            except Vessel.DoesNotExist:
                errors["codigo_buque"] = f"Vaixell '{self.codigo_buque}' no trobat al catàleg"

        # Validar port (si té puerto_al5, podríem validar-lo també)
        # Nota: puerto_al5 no és directament el code de Port, caldria lògica addicional

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Validar abans de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "buque"
        verbose_name = "Vaixell"
        verbose_name_plural = "Vaixells"
        indexes = [
            models.Index(fields=["vessel_ref"]),
            models.Index(fields=["port_ref"]),
        ]
        # constraints = [
        #    CheckConstraint(
        #        check=Q(unidad_productiva__metodo_produccion__in=[1, 4]),
        #        name='buque_metodo_produccion_valido'
        #    )
        # ]

    def __str__(self):
        return f"Vaixell {self.codigo_buque}"


class Granja(models.Model):
    """
    Dades específiques per granges d'aqüicultura
    """

    unidad_productiva = models.OneToOneField(
        UnidadProductiva, on_delete=models.CASCADE, primary_key=True, related_name="granja"
    )

    codigo_rega = models.CharField(max_length=14, db_index=True, help_text="Codi REGA de la granja")

    lugar_descarga = models.CharField(max_length=250, blank=True, help_text="Lloc de descàrrega")

    fecha_produccion = models.DateTimeField(help_text="Data de producció")

    class Meta:
        db_table = "granja"
        verbose_name = "Granja"
        verbose_name_plural = "Granges"
        # constraints = [
        #    CheckConstraint(
        #        check=Q(unidad_productiva__metodo_produccion=2),
        #        name='granja_metodo_produccion_valido'
        #    )
        # ]

    def __str__(self):
        return f"Granja {self.codigo_rega}"


class PersonaFisicaJuridica(models.Model):
    """
    Dades específiques per persones físiques o jurídiques
    """

    unidad_productiva = models.OneToOneField(
        UnidadProductiva, on_delete=models.CASCADE, primary_key=True, related_name="persona"
    )

    nif_persona = models.CharField(max_length=17, db_index=True, help_text="NIF/NIE/CIF de la persona")

    lugar_descarga = models.CharField(max_length=250, blank=True, help_text="Lloc de descàrrega")

    fecha_descarga = models.DateTimeField(help_text="Data de descàrrega")

    class Meta:
        db_table = "persona_fisica_juridica"
        verbose_name = "Persona física/jurídica"
        verbose_name_plural = "Persones físiques/jurídiques"
        # constraints = [
        #    CheckConstraint(
        #        check=Q(unidad_productiva__metodo_produccion__in=[1, 3, 4]),
        #        name='persona_metodo_produccion_valido'
        #    )
        # ]

    def __str__(self):
        return f"Persona {self.nif_persona}"


"""
Models per Espècies i Dates de Captura
Segona part dels models de sales_notes
"""


class Especie(TimeStampedModel):
    """
    Espècie venuda amb tota la informació associada
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unidad_productiva = models.ForeignKey("UnidadProductiva", on_delete=models.CASCADE, related_name="especies")

    # Identificació de la venda
    num_doc_venta = models.CharField(max_length=21, db_index=True, help_text="Número del document de venda")

    # Espècie
    codigo_al3_validator = RegexValidator(regex=r"^[A-Za-z]{3}$", message="Codi AL3 invàlid (ha de ser 3 lletres)")
    species_ref = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        to_field="code_3a",
        related_name="ventas",
        null=True,
        blank=True,
        help_text="Referència a l'espècie del catàleg",
    )
    especie_al3 = models.CharField(
        max_length=3, validators=[codigo_al3_validator], db_index=True, help_text="Codi FAO de l'espècie (3 lletres)"
    )

    # Zona de captura
    zona = models.CharField(max_length=50, blank=True)
    zona_geografica = models.CharField(max_length=50, blank=True)

    ccaa = models.IntegerField(null=True, blank=True, help_text="Codi Comunitat Autònoma")

    pais_al3 = models.CharField(
        max_length=3, validators=[codigo_al3_validator], blank=True, help_text="Codi ISO-3 del país"
    )

    masa_agua = models.CharField(max_length=100, blank=True, help_text="Massa d'aigua on es va capturar")

    # Art de pesca
    arte_al3 = models.CharField(max_length=3, blank=True, db_index=True, help_text="Codi d'art de pesca (FAO)")

    otro_arte = models.CharField(max_length=100, blank=True, help_text="Descripció d'altres arts no estandarditzats")

    # Presentació i estat del producte
    cod_especie_conservacion = models.CharField(max_length=3, blank=True, help_text="Codi estat de conservació")

    cod_especie_presentacion = models.CharField(max_length=5, blank=True, help_text="Codi presentació del producte")

    presentacion_oth = models.CharField(max_length=50, blank=True, help_text="Altres presentacions")

    id_presentacion_oth = models.IntegerField(null=True, blank=True)

    cod_especie_frescura = models.CharField(max_length=2, blank=True, help_text="Codi frescura")

    cod_especie_calibre = models.CharField(max_length=15, blank=True, help_text="Codi calibre")

    # Data de venda
    fecha_venta = models.DateTimeField(db_index=True, help_text="Data i hora de venda")

    lote = models.CharField(max_length=50, blank=True, help_text="Número de lot")

    cod_contrato_alim = models.CharField(max_length=50, blank=True, help_text="Codi contracte alimentari")

    # Documents associats
    num_doc_transporte = models.CharField(max_length=50, blank=True, help_text="Número document de transport")

    num_declaracion_recog = models.CharField(max_length=21, blank=True, help_text="Número declaració recollida")

    certificado_de_origen = models.BooleanField(default=False, help_text="Té certificat d'origen")

    # Venedor
    TIPO_NIF_CHOICES = [
        (1, "NIF"),
        (2, "NIE"),
        (3, "Passaport"),
        (5, "Altres documents"),
    ]

    tipo_cif_nif_vendedor = models.IntegerField(
        choices=TIPO_NIF_CHOICES, help_text="Tipus document identificació venedor"
    )

    nif_vendedor = models.CharField(max_length=17, db_index=True, help_text="NIF/CIF del venedor")

    nombre_vendedor = models.CharField(max_length=100, help_text="Nom del venedor")

    direccion_vendedor = models.CharField(max_length=100, blank=True, help_text="Direcció del venedor")

    # Comprador
    nif_comprador = models.CharField(max_length=17, db_index=True, help_text="NIF/CIF del comprador")

    id_tipo_nif_cif_comprador = models.IntegerField(
        choices=TIPO_NIF_CHOICES, help_text="Tipus document identificació comprador"
    )

    pais_comprador_validator = RegexValidator(regex=r"^[A-Za-z]{3}$", message="Codi país invàlid (ISO-3, 3 lletres)")
    pais_comprador = models.CharField(
        max_length=3, validators=[pais_comprador_validator], blank=True, help_text="Codi ISO-3 país del comprador"
    )

    nombre_comprador = models.CharField(max_length=100, help_text="Nom del comprador")

    direccion_comprador = models.CharField(max_length=100, blank=True, help_text="Direcció del comprador")

    # Informació econòmica
    precio = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))], help_text="Preu total"
    )

    cod_moneda_validator = RegexValidator(regex=r"^[A-Za-z]{3}$", message="Codi moneda invàlid (ISO-4217, 3 lletres)")
    cod_moneda = models.CharField(
        max_length=3, default="EUR", validators=[cod_moneda_validator], help_text="Codi ISO-4217 moneda"
    )

    # Quantitats
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal("0.001"))], help_text="Quantitat en kg"
    )

    num_ejemplares = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)], help_text="Nombre d'exemplars"
    )

    num_cajas = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)], help_text="Nombre de caixes"
    )

    es_talla_reglamentaria = models.BooleanField(default=True, help_text="És talla reglamentària")

    # Retirada
    TIPO_RETIRADA_CHOICES = [
        (1, "No s'ha retirat"),
        (2, "Retirada per talla"),
        (3, "Retirada per quota"),
        (4, "Retirada sense preu"),
        (5, "Retirada altre"),
        (6, "Desembarcament per sota mínims"),
    ]

    tipo_retirada = models.IntegerField(
        choices=TIPO_RETIRADA_CHOICES, null=True, blank=True, help_text="Tipus de retirada"
    )

    cod_destino_retirado = models.CharField(max_length=50, blank=True, help_text="Codi destí del producte retirat")

    # Emmagatzematge i observacions
    lugar_almacenamiento = models.CharField(max_length=100, blank=True, help_text="Lloc d'emmagatzematge")

    observaciones = models.TextField(blank=True, help_text="Observacions addicionals")

    num_acta_inspeccion = models.CharField(max_length=20, blank=True, help_text="Número d'acta d'inspecció")

    def clean(self):
        """Validar i sincronitzar espècie amb catàleg"""

        if self.especie_al3:
            try:
                # Buscar l'espècie al catàleg
                species = Species.objects.get(code_3a=self.especie_al3)
                self.species_ref = species
            except Species.DoesNotExist:
                raise ValidationError({"especie_al3": f"Espècie '{self.especie_al3}' no trobada al catàleg"})

    def save(self, *args, **kwargs):
        """Validar abans de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "especie"
        ordering = ["-fecha_venta"]
        verbose_name = "Espècie"
        verbose_name_plural = "Espècies"
        indexes = [
            models.Index(fields=["especie_al3", "fecha_venta"]),
            models.Index(fields=["species_ref", "fecha_venta"]),
            models.Index(fields=["arte_al3", "zona"]),
            models.Index(fields=["nif_vendedor", "fecha_venta"]),
            models.Index(fields=["nif_comprador", "fecha_venta"]),
        ]

    def __str__(self):
        return f"{self.especie_al3} - {self.num_doc_venta} ({self.cantidad} kg)"

    @property
    def precio_por_kg(self):
        """Calcula el preu per kg"""
        if self.cantidad > 0:
            return self.precio / self.cantidad
        return Decimal("0.00")


class FechaCaptura(models.Model):
    """
    Dates de captura associades a una espècie
    Pot haver-hi múltiples períodes de captura per espècie
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="fechas_captura")

    fecha_captura_ini = models.DateTimeField(help_text="Data i hora inici captura")

    fecha_captura_fin = models.DateTimeField(null=True, blank=True, help_text="Data i hora fi captura (opcional)")

    class Meta:
        db_table = "fecha_captura"
        ordering = ["fecha_captura_ini"]
        verbose_name = "Data de captura"
        verbose_name_plural = "Dates de captura"
        indexes = [
            models.Index(fields=["fecha_captura_ini", "fecha_captura_fin"]),
        ]

    def __str__(self):
        if self.fecha_captura_fin:
            return f"{self.fecha_captura_ini} - {self.fecha_captura_fin}"
        return f"{self.fecha_captura_ini}"


# Importar TimeStampedModel del fitxer anterior
from .models import TimeStampedModel
