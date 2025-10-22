"""
Models per taules existents que NO volem que Django gestioni
Aquestes taules ja existeixen a la BD i només les llegim
"""
from django.contrib.gis.db import models


class Port(models.Model):
    """Taula existent de ports"""
    id = models.SmallIntegerField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=50, db_column='Name')
    region = models.CharField(max_length=50, null=True, blank=True, db_column='Region')
    area = models.CharField(max_length=50, null=True, blank=True, db_column='Area')
    latitude = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True, db_column='Latitude')
    longitude = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True, db_column='Longitude')
    code = models.IntegerField(db_column='Code')
    geom = models.GeometryField(null=True, blank=True, db_column='geom')
    autonomous_community = models.CharField(max_length=50, null=True, blank=True, db_column='AutonomousCommunity')
    fishers_association = models.BooleanField(null=True, blank=True, db_column='FishersAssociation')
    auction = models.BooleanField(null=True, blank=True, db_column='Auction')
    
    class Meta:
        managed = False 
        db_table = 'port'
        verbose_name = 'Port'
        verbose_name_plural = 'Ports'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Species(models.Model):
    """Taula existent d'espècies"""
    id = models.IntegerField(primary_key=True, db_column='Id')
    code_3a = models.CharField(max_length=3, null=True, blank=True, db_column='3A_Code')
    scientific_name = models.CharField(max_length=37, db_column='ScientificName')
    catalan_name = models.CharField(max_length=30, null=True, blank=True, db_column='CatalanName')
    spanish_name = models.CharField(max_length=30, null=True, blank=True, db_column='SpanishName')
    english_name = models.CharField(max_length=30, null=True, blank=True, db_column='EnglishName')
    group = models.CharField(max_length=50, null=True, blank=True, db_column='Group')
    group2 = models.CharField(max_length=50, null=True, blank=True, db_column='Group2')
    french_name = models.CharField(max_length=30, null=True, blank=True, db_column='FrenchName')
    generalitat_name = models.CharField(max_length=100, null=True, blank=True, db_column='GeneralitatName')
    species_class = models.CharField(max_length=30, null=True, blank=True, db_column='Class')
    order = models.CharField(max_length=30, null=True, blank=True, db_column='Order')
    family = models.CharField(max_length=30, null=True, blank=True, db_column='Family')
    genus = models.CharField(max_length=30, null=True, blank=True, db_column='Genus')
    a_const = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, db_column='A_Const')
    b_const = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, db_column='B_Const')
    generalitat_code = models.CharField(max_length=3, null=True, blank=True, db_column='GeneralitatCode')
    observations = models.TextField(null=True, blank=True, db_column='Observations')
    minimum_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='MinimumSize')
    maximum_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='MaximumSize')
    number_of_sizes = models.IntegerField(null=True, blank=True, db_column='NumberOfSizes')
    is_waste = models.BooleanField(null=True, blank=True, db_column='IsWaste')
    waste_type = models.CharField(max_length=30, null=True, blank=True, db_column='WasteType')
    phylum = models.CharField(max_length=30, null=True, blank=True, db_column='Phylum')
    taxonomic_group = models.CharField(max_length=30, null=True, blank=True, db_column='TaxonomicGroup')
    mcrs = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='MCRS')
    aphia_id = models.IntegerField(null=True, blank=True, db_column='AphiaId')
    
    class Meta:
        managed = False
        db_table = 'species'
        verbose_name = 'Espècie'
        verbose_name_plural = 'Espècies'
    
    def __str__(self):
        return f"{self.code_3a} - {self.scientific_name}"


class Vessel(models.Model):
    """Taula existent de vaixells"""
    id = models.IntegerField(primary_key=True, db_column='Id')
    code = models.CharField(max_length=12, null=True, blank=True, db_column='Code')
    event_code = models.CharField(max_length=3, null=True, blank=True, db_column='EventCode')
    event_start_date = models.DateField(null=True, blank=True, db_column='EventStartDate')
    event_end_date = models.DateField(null=True, blank=True, db_column='EventEndDate')
    licence_ind = models.BooleanField(null=True, blank=True, db_column='LicenceInd')
    registration_num = models.CharField(max_length=15, null=True, blank=True, db_column='RegistrationNum')
    name = models.CharField(max_length=50, null=True, blank=True, db_column='Name')
    base_port_code = models.IntegerField(null=True, blank=True, db_column='BasePortCode')
    base_port_name = models.CharField(max_length=30, null=True, blank=True, db_column='BasePortName')
    ircs = models.CharField(max_length=10, null=True, blank=True, db_column='IRCS')
    vms = models.BooleanField(null=True, blank=True, db_column='VMS')
    gear_main_code = models.CharField(max_length=3, null=True, blank=True, db_column='GearMainCode')
    gear_sec_code = models.CharField(max_length=3, null=True, blank=True, db_column='GearSecCode')
    loa_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='LOA_m')
    gt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='GT')
    power_main_kw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='PowerMain_kW')
    hull_material = models.CharField(max_length=20, null=True, blank=True, db_column='HullMaterial')
    service_starting_date = models.DateField(null=True, blank=True, db_column='ServiceStartingDate')
    base_port_id = models.SmallIntegerField(null=True, blank=True, db_column='BasePortId')
    ais = models.BooleanField(null=True, blank=True, db_column='AIS')
    
    class Meta:
        managed = False
        db_table = 'vessel'
        verbose_name = 'Vaixell'
        verbose_name_plural = 'Vaixells'
    
    def __str__(self):
        return f"{self.code} - {self.name}"