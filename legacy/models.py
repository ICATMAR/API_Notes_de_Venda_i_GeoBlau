# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class VcpeAutoDownload(models.Model):
    vesselcode = models.CharField(db_column="VesselCode", max_length=12, blank=True, null=True)
    vesselname = models.CharField(db_column="VesselName", max_length=50, blank=True, null=True)
    vesseltype = models.CharField(db_column="VesselType", max_length=30, blank=True, null=True)
    salenumber = models.CharField(db_column="SaleNumber", max_length=30, blank=True, null=True)
    lot = models.CharField(db_column="Lot", max_length=30, blank=True, null=True)
    calibre = models.CharField(db_column="Calibre", max_length=40, blank=True, null=True)
    size = models.CharField(db_column="Size", max_length=20, blank=True, null=True)
    doctype = models.CharField(db_column="DocType", max_length=10, blank=True, null=True)
    speciecode = models.CharField(db_column="SpecieCode", max_length=3, blank=True, null=True)
    speciename = models.CharField(db_column="SpecieName", max_length=30, blank=True, null=True)
    portname = models.CharField(db_column="PortName", max_length=50, blank=True, null=True)
    date = models.DateField(db_column="Date", blank=True, null=True)
    porttype = models.CharField(db_column="PortType", max_length=40, blank=True, null=True)
    freshness = models.CharField(db_column="Freshness", max_length=20, blank=True, null=True)
    presentation = models.CharField(db_column="Presentation", max_length=50, blank=True, null=True)
    conservation = models.CharField(db_column="Conservation", max_length=20, blank=True, null=True)
    fishingartcode = models.CharField(db_column="FishingArtCode", max_length=10, blank=True, null=True)
    fishingartname = models.CharField(db_column="FishingArtName", max_length=100, blank=True, null=True)
    vesselownercode = models.CharField(db_column="VesselOwnerCode", max_length=50, blank=True, null=True)
    otherfishingarts = models.CharField(db_column="OtherFishingArts", max_length=30, blank=True, null=True)
    weight = models.DecimalField(db_column="Weight", max_digits=20, decimal_places=3, blank=True, null=True)
    amount = models.DecimalField(db_column="Amount", max_digits=20, decimal_places=4, blank=True, null=True)
    id = models.BigAutoField(db_column="Id", primary_key=True)
    portid = models.ForeignKey("Port", models.DO_NOTHING, db_column="PortId", blank=True, null=True)
    vesselid = models.IntegerField(db_column="VesselId", blank=True, null=True)
    specieid = models.IntegerField(db_column="SpecieId", blank=True, null=True)
    baseportcode = models.IntegerField(db_column="BasePortCode", blank=True, null=True)
    baseportname = models.CharField(db_column="BasePortName", max_length=50, blank=True, null=True)
    baseportid = models.ForeignKey("PortAll", models.DO_NOTHING, db_column="BasePortId", blank=True, null=True)
    metiercat = models.CharField(db_column="MetierCAT", max_length=30, blank=True, null=True)
    metierdcf = models.CharField(db_column="MetierDCF", max_length=10, blank=True, null=True)
    trackcode = models.CharField(db_column="TrackCode", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "vcpe_auto_download"
        verbose_name = "VCPE Auto Download"

    def __str__(self):
        return f"{self.vesselname} - {self.speciename} ({self.date})"


class Vessel(models.Model):
    code = models.CharField(db_column="Code", unique=True, max_length=12, blank=True, null=True)
    eventcode = models.CharField(db_column="EventCode", max_length=3, blank=True, null=True)
    eventstartdate = models.DateField(db_column="EventStartDate", blank=True, null=True)
    eventenddate = models.DateField(db_column="EventEndDate", blank=True, null=True)
    licenceind = models.BooleanField(db_column="LicenceInd", blank=True, null=True)
    registrationnum = models.CharField(db_column="RegistrationNum", max_length=15, blank=True, null=True)
    name = models.CharField(db_column="Name", max_length=50, blank=True, null=True)
    baseportcode = models.IntegerField(db_column="BasePortCode", blank=True, null=True)
    baseportname = models.CharField(db_column="BasePortName", max_length=30, blank=True, null=True)
    ircs = models.CharField(db_column="IRCS", max_length=10, blank=True, null=True)
    vms = models.BooleanField(db_column="VMS", blank=True, null=True)
    gearmaincode = models.CharField(db_column="GearMainCode", max_length=3, blank=True, null=True)
    gearseccode = models.CharField(db_column="GearSecCode", max_length=3, blank=True, null=True)
    loa_m = models.DecimalField(db_column="LOA_m", max_digits=10, decimal_places=2, blank=True, null=True)
    lbp_m = models.DecimalField(db_column="LBP_m", max_digits=10, decimal_places=2, blank=True, null=True)
    gt = models.DecimalField(db_column="GT", max_digits=10, decimal_places=2, blank=True, null=True)
    trb = models.DecimalField(db_column="TRB", max_digits=10, decimal_places=2, blank=True, null=True)
    powermain_kw = models.DecimalField(db_column="PowerMain_kW", max_digits=10, decimal_places=2, blank=True, null=True)
    poweraux_kw = models.DecimalField(db_column="PowerAux_kW", max_digits=10, decimal_places=2, blank=True, null=True)
    hullmaterial = models.CharField(db_column="HullMaterial", max_length=20, blank=True, null=True)
    servicestartingdate = models.DateField(db_column="ServiceStartingDate", blank=True, null=True)
    # Canviat de Integer a ForeignKey per permetre relacions
    baseportid = models.ForeignKey(
        "Port", models.DO_NOTHING, db_column="BasePortId", blank=True, null=True, related_name="vessels"
    )
    ais = models.BooleanField(db_column="AIS", blank=True, null=True)
    id = models.AutoField(db_column="Id", primary_key=True)

    class Meta:
        managed = False
        db_table = "vessel"
        verbose_name = "Vaixell"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Port(models.Model):
    id = models.SmallAutoField(db_column="Id", primary_key=True)
    name = models.CharField(db_column="Name", max_length=50)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    area = models.CharField(db_column="Area", max_length=50, blank=True, null=True)
    latitude = models.DecimalField(db_column="Latitude", max_digits=15, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(db_column="Longitude", max_digits=15, decimal_places=8, blank=True, null=True)
    code = models.IntegerField(db_column="Code")
    geom = models.GeometryField(srid=0, blank=True, null=True)
    autonomouscommunity = models.CharField(db_column="AutonomousCommunity", max_length=50, blank=True, null=True)
    fishersassociation = models.BooleanField(db_column="FishersAssociation", blank=True, null=True)
    auction = models.BooleanField(db_column="Auction", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "port"
        verbose_name = "Port"

    def __str__(self):
        return self.name


class Species(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    number_3a_code = models.CharField(db_column="3A_Code", unique=True, max_length=3, blank=True, null=True)
    scientificname = models.CharField(db_column="ScientificName", unique=True, max_length=37)
    catalanname = models.CharField(db_column="CatalanName", max_length=30, blank=True, null=True)
    spanishname = models.CharField(db_column="SpanishName", max_length=30, blank=True, null=True)
    englishname = models.CharField(db_column="EnglishName", max_length=30, blank=True, null=True)
    group = models.CharField(db_column="Group", max_length=50, blank=True, null=True)
    group2 = models.CharField(db_column="Group2", max_length=50, blank=True, null=True)
    frenchname = models.CharField(db_column="FrenchName", max_length=30, blank=True, null=True)
    generalitatname = models.CharField(db_column="GeneralitatName", max_length=100, blank=True, null=True)
    class_field = models.CharField(db_column="Class", max_length=30, blank=True, null=True)
    order = models.CharField(db_column="Order", max_length=30, blank=True, null=True)
    family = models.CharField(db_column="Family", max_length=30, blank=True, null=True)
    genus = models.CharField(db_column="Genus", max_length=30, blank=True, null=True)
    a_const = models.DecimalField(db_column="A_Const", max_digits=12, decimal_places=4, blank=True, null=True)
    b_const = models.DecimalField(db_column="B_Const", max_digits=12, decimal_places=4, blank=True, null=True)
    generalitatcode = models.CharField(db_column="GeneralitatCode", max_length=3, blank=True, null=True)
    observations = models.TextField(db_column="Observations", blank=True, null=True)
    minimumsize = models.DecimalField(db_column="MinimumSize", max_digits=12, decimal_places=2, blank=True, null=True)
    maximumsize = models.DecimalField(db_column="MaximumSize", max_digits=12, decimal_places=2, blank=True, null=True)
    numberofsizes = models.IntegerField(db_column="NumberOfSizes", blank=True, null=True)
    iswaste = models.BooleanField(db_column="IsWaste", blank=True, null=True)
    wastetype = models.CharField(db_column="WasteType", max_length=30, blank=True, null=True)
    phylum = models.CharField(db_column="Phylum", max_length=30, blank=True, null=True)
    taxonomicgroup = models.CharField(db_column="TaxonomicGroup", max_length=30, blank=True, null=True)
    demersal = models.BooleanField(db_column="Demersal", blank=True, null=True)
    pelagic = models.BooleanField(db_column="Pelagic", blank=True, null=True)
    hardseabed = models.BooleanField(db_column="HardSeabed", blank=True, null=True)
    softseabed = models.BooleanField(db_column="SoftSeabed", blank=True, null=True)
    bothseabed = models.BooleanField(db_column="BothSeabed", blank=True, null=True)
    cartilaginous = models.BooleanField(db_column="Cartilaginous", blank=True, null=True)
    bony = models.BooleanField(db_column="Bony", blank=True, null=True)
    r = models.SmallIntegerField(db_column="R", blank=True, null=True)
    g = models.SmallIntegerField(db_column="G", blank=True, null=True)
    b = models.SmallIntegerField(db_column="B", blank=True, null=True)
    mcrs = models.DecimalField(db_column="MCRS", max_digits=12, decimal_places=2, blank=True, null=True)
    l50 = models.DecimalField(db_column="L50", max_digits=12, decimal_places=2, blank=True, null=True)
    l50female = models.DecimalField(db_column="L50Female", max_digits=12, decimal_places=2, blank=True, null=True)
    l50male = models.DecimalField(db_column="L50Male", max_digits=12, decimal_places=2, blank=True, null=True)
    aphiaid = models.IntegerField(db_column="AphiaId", blank=True, null=True)
    projectid = models.IntegerField(db_column="ProjectId", blank=True, null=True)
    codi_medits = models.TextField(blank=True, null=True)
    categoria_medits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "species"
        verbose_name = "Espècie"

    def __str__(self):
        return f"{self.scientificname} ({self.number_3a_code})"


class PortAll(models.Model):
    name = models.CharField(db_column="Name", max_length=50, blank=True, null=True)
    region = models.CharField(db_column="Region", max_length=50, blank=True, null=True)
    area = models.CharField(db_column="Area", max_length=50, blank=True, null=True)
    latitude = models.DecimalField(db_column="Latitude", max_digits=15, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(db_column="Longitude", max_digits=15, decimal_places=8, blank=True, null=True)
    code = models.IntegerField(db_column="Code", blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)
    autonomouscommunity = models.CharField(db_column="AutonomousCommunity", max_length=50, blank=True, null=True)
    id = models.SmallAutoField(db_column="Id", primary_key=True)
    al5 = models.CharField(db_column="AL5", max_length=5, blank=True, null=True)
    fishersassociation = models.BooleanField(db_column="FishersAssociation", blank=True, null=True)
    auction = models.BooleanField(db_column="Auction", blank=True, null=True)
    gsa = models.CharField(db_column="GSA", blank=True, null=True)
    country = models.CharField(db_column="Country", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "port_all"
        verbose_name = "Port All"

    def __str__(self):
        return self.name
