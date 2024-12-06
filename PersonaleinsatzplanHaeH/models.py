from django.db import models
from django.urls import reverse
from django.db.models import Sum

class Niederlassung(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Position(models.Model):
    bezeichnung = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.bezeichnung

class Mitarbeiter(models.Model):
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    qualifikation = models.CharField(max_length=255)
    max_woechentliche_arbeitszeit = models.IntegerField()
    personalnummer = models.IntegerField(unique=True, null=False)
    geburtsdatum = models.DateField()
    vertragsbeginn = models.DateField()
    vertragsendeBefristet = models.DateField(blank=True, null=True)
    unbefristet = models.BooleanField(default=False)
    niederlassung = models.ForeignKey(Niederlassung, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiter_detail', args=[str(self.id)])


class PersonaleinsatzplanStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Personaleinsatzplan(models.Model):
    STATUS_CHOICES = [
        ('entwurf', 'Entwurf'),
        ('in_bearbeitung', 'in Bearbeitung'),
        ('gueltig', 'Gültig'),
        ('archiviert', 'Archiviert'),
        ('storniert', 'Storniert')
    ]

    name = models.CharField(max_length=255)
    gueltigkeit_monat = models.IntegerField(choices=[
        (1, "Januar"), (2, "Februar"), (3, "März"), (4, "April"),
        (5, "Mai"), (6, "Juni"), (7, "Juli"), (8, "August"),
        (9, "September"), (10, "Oktober"), (11, "November"), (12, "Dezember")
    ])
    gueltigkeit_jahr = models.IntegerField()
    kostentraeger = models.CharField(max_length=255)
    ersteller = models.CharField(max_length=255)
    version = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='entwurf')
    niederlassung = models.ForeignKey(
        'Niederlassung', on_delete=models.PROTECT, related_name='personaleinsatzplaene'
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        monat_choices = dict(self._meta.get_field('gueltigkeit_monat').choices)
        monat = monat_choices.get(self.gueltigkeit_monat, "Unbekannt")

        self.name = f"Personaleinsatzplan {self.niederlassung.name} - {monat} {self.gueltigkeit_jahr}"
        super().save(*args, **kwargs)


class Auftrag(models.Model):
    name = models.CharField(max_length=255)
    vergabenummer = models.CharField(max_length=255, unique=True)
    optionsnummer = models.CharField(max_length=255, unique=True)
    massnahmenummer = models.CharField(max_length=255, unique=True)
    startdatum = models.DateField()
    enddatum = models.DateField()
    max_klienten = models.IntegerField(default=0)
    mindest_klienten = models.IntegerField(default=0)
    aktuell_klienten = models.IntegerField(default=0)
    personaleinsatzplan = models.ForeignKey(Personaleinsatzplan, on_delete=models.CASCADE, related_name='auftraege')

    def __str__(self):
        return self.name


class Betreuungsschluessel(models.Model):
    name = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    klienten_pro_betreuer = models.IntegerField()
    auftrag = models.ForeignKey(Auftrag, on_delete=models.CASCADE, related_name='betreuungsschluessel', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def abgedeckte_VZA(self):
        total_stunden = MitarbeiterBetreuungsschluessel.objects.filter(
            schluessel=self
        ).aggregate(total=Sum('anteil_stunden_pro_woche'))['total']

        vza_wert = VollzeitaequivalentStunden.objects.first().wert if VollzeitaequivalentStunden.objects.exists() else 1
        abgedeckte_vza = (total_stunden / vza_wert) if total_stunden else 0
        return round(abgedeckte_vza, 1)

    @property
    def benoetigte_VZA_max(self):
        if self.auftrag:
            return self.auftrag.max_klienten / self.klienten_pro_betreuer
        return 0

    @property
    def benoetigte_VZA_mindest(self):
        if self.auftrag:
            return self.auftrag.mindest_klienten / self.klienten_pro_betreuer
        return 0

    @property
    def benoetigte_VZA_aktuell(self):
        if self.auftrag:
            return self.auftrag.aktuell_klienten / self.klienten_pro_betreuer
        return 0

    @property
    def differenz_VZA_max(self):
        return round(self.benoetigte_VZA_max - self.abgedeckte_VZA, 1)

    @property
    def differenz_VZA_mindest(self):
        return round(self.benoetigte_VZA_mindest - self.abgedeckte_VZA, 1)

    @property
    def differenz_VZA_aktuell(self):
        return round(self.benoetigte_VZA_aktuell - self.abgedeckte_VZA, 1)


class MitarbeiterBetreuungsschluessel(models.Model):
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    anteil_stunden_pro_woche = models.FloatField()
    kommentar = models.TextField(blank=True, null=True)
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.PROTECT, related_name='betreuungsschluessel_zuweisungen')
    schluessel = models.ForeignKey(Betreuungsschluessel, on_delete=models.PROTECT, related_name='mitarbeiter_zuweisungen')
    auftrag = models.ForeignKey(Auftrag, on_delete=models.PROTECT, related_name='mitarbeiter_betreuungsschluessel')
    freie_stunden = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.mitarbeiter} - {self.schluessel}"

    @staticmethod
    def calculate_hours_and_free_time(mitarbeiter, personaleinsatzplan):

        if not mitarbeiter or not personaleinsatzplan:
            return {"total_hours": 0, "free_hours": 0}

        # Summe der Stunden pro Woche berechnen
        queryset = MitarbeiterBetreuungsschluessel.objects.filter(
            mitarbeiter=mitarbeiter,
            schluessel__auftrag__personaleinsatzplan__gueltigkeit_monat=personaleinsatzplan.gueltigkeit_monat,
            schluessel__auftrag__personaleinsatzplan__gueltigkeit_jahr=personaleinsatzplan.gueltigkeit_jahr,
            schluessel__auftrag__personaleinsatzplan__status=personaleinsatzplan.status,
        )

        aggregation_result = queryset.aggregate(total_stunden=Sum('anteil_stunden_pro_woche'))

        total_hours = aggregation_result['total_stunden'] or 0

        max_arbeitszeit = mitarbeiter.max_woechentliche_arbeitszeit

        free_hours = max_arbeitszeit - total_hours

        return {"total_hours": total_hours, "free_hours": free_hours}


class VollzeitaequivalentStunden(models.Model):
    wert = models.IntegerField()

    def __str__(self):
        return str(self.wert)






