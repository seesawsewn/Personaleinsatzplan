from datetime import date

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Sum

class Niederlassung(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:niederlassung_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:niederlassung_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:niederlassung_delete', args=[str(self.id)])


class Position(models.Model):
    bezeichnung = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.bezeichnung

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:position_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:position_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:position_delete', args=[str(self.id)])


class Mitarbeiter(models.Model):
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    qualifikation = models.CharField(max_length=255, blank=True, null=True)
    max_woechentliche_arbeitszeit = models.IntegerField()
    personalnummer = models.IntegerField(unique=True, null=False)
    geburtsdatum = models.DateField(blank=True, null=True)
    vertragsbeginn = models.DateField(blank=True, null=True)
    vertragsendeBefristet = models.DateField(blank=True, null=True)
    unbefristet = models.BooleanField(default=False)
    niederlassung = models.ForeignKey(Niederlassung, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiter_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiter_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiter_delete', args=[str(self.id)])


class PersonaleinsatzplanStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplanstatus_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplanstatus_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplanstatus_delete', args=[str(self.id)])


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
    ])  # Werte 1-12 für Januar-Dezember
    gueltigkeit_jahr = models.IntegerField()  # Für das Jahr, z.B. 2024
    kostentraeger = models.CharField(max_length=255)
    ersteller = models.CharField(max_length=255)
    version = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='entwurf')
    niederlassung = models.ForeignKey(
        'Niederlassung', on_delete=models.PROTECT, null=True, blank=True, related_name='personaleinsatzplaene'
    )

    def __str__(self):
        # Gibt den Monatsnamen und das Jahr aus, z.B. "März 2024"
        return f"{self.name} - {self.get_gueltigkeit_monat_display()} {self.gueltigkeit_jahr}"

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_delete', args=[str(self.id)])


class Auftrag(models.Model):
    name = models.CharField(max_length=255)
    vergabenummer = models.IntegerField(unique=True, blank=True, null=True)
    optionsnummer = models.IntegerField(unique=True, blank=True, null=True)
    massnahmenummer = models.IntegerField(unique=True, blank=True, null=True)
    startdatum = models.DateField(blank=True, null=True)
    enddatum = models.DateField(blank=True, null=True)
    max_klienten = models.IntegerField(default=0)
    mindest_klienten = models.IntegerField(default=0)
    aktuell_klienten = models.IntegerField(default=0)
    personaleinsatzplan = models.ForeignKey(Personaleinsatzplan, on_delete=models.CASCADE, related_name='auftraege', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:auftrag_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:auftrag_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:auftrag_delete', args=[str(self.id)])


class Betreuungsschluessel(models.Model):
    name = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True, blank=True)
    klienten_pro_betreuer = models.IntegerField()
    auftrag = models.ForeignKey(Auftrag, on_delete=models.CASCADE, related_name='betreuungsschluessel', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_delete', args=[str(self.id)])

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
    position = models.ForeignKey(Position, on_delete=models.PROTECT, null=True, blank=True)
    anteil_stunden_pro_woche = models.FloatField()
    kommentar = models.TextField(blank=True, null=True)
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.PROTECT, null=True, blank=True, related_name='betreuungsschluessel_zuweisungen')
    schluessel = models.ForeignKey(Betreuungsschluessel, on_delete=models.PROTECT, null=True, blank=True, related_name='mitarbeiter_zuweisungen')
    auftrag = models.ForeignKey(Auftrag, on_delete=models.PROTECT, null=True, blank=True, related_name='mitarbeiter_betreuungsschluessel')
    zugewiesene_stunden = models.FloatField(default=0)  # Summe aller Stunden, die dem Mitarbeiter zugeordnet wurden
    freie_stunden = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.mitarbeiter} - {self.schluessel}"

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_delete', args=[str(self.id)])

    @staticmethod
    def calculate_hours_and_free_time(mitarbeiter, personaleinsatzplan):
        """
        Berechnet die Summe aller `anteil_stunden_pro_woche` eines Mitarbeiters (`total_hours`) und die freien Stunden
        (`free_hours`) basierend auf der maximalen Arbeitszeit (`max_woechentliche_arbeitszeit`).

        Freie Stunden = max_woechentliche_arbeitszeit - Summe der `anteil_stunden_pro_woche`.
        """
        if not mitarbeiter or not personaleinsatzplan:
            print("Berechnung abgebrochen: Mitarbeiter oder Personaleinsatzplan fehlt.")
            return {"total_hours": 0, "free_hours": 0}

        # Debugging: Personaleinsatzplan-Werte prüfen
        print(f"Personaleinsatzplan Monat: {personaleinsatzplan.gueltigkeit_monat}")
        print(f"Personaleinsatzplan Jahr: {personaleinsatzplan.gueltigkeit_jahr}")
        print(f"Personaleinsatzplan Status: {personaleinsatzplan.status}")

        # Summe der Stunden pro Woche berechnen
        queryset = MitarbeiterBetreuungsschluessel.objects.filter(
            mitarbeiter=mitarbeiter,
            schluessel__auftrag__personaleinsatzplan__gueltigkeit_monat=personaleinsatzplan.gueltigkeit_monat,
            schluessel__auftrag__personaleinsatzplan__gueltigkeit_jahr=personaleinsatzplan.gueltigkeit_jahr,
            schluessel__auftrag__personaleinsatzplan__status=personaleinsatzplan.status,
        )
        print("Generierter SQL-Query:", queryset.query)

        # Debugging: Alle Einträge im QuerySet und deren `anteil_stunden_pro_woche` anzeigen
        for eintrag in queryset:
            print(f"Mitarbeiter: {eintrag.mitarbeiter}, Betreuungsschlüssel: {eintrag.schluessel}, "
                  f"Anteil Stunden pro Woche: {eintrag.anteil_stunden_pro_woche}")

        # Aggregation durchführen
        aggregation_result = queryset.aggregate(total_stunden=Sum('anteil_stunden_pro_woche'))
        print("Aggregationsergebnis:", aggregation_result)

        total_hours = aggregation_result['total_stunden'] or 0
        print(f"Aggregierte Stunden pro Woche für Mitarbeiter {mitarbeiter}: {total_hours}")

        # Maximale Arbeitszeit des Mitarbeiters abrufen
        max_arbeitszeit = mitarbeiter.max_woechentliche_arbeitszeit

        # Berechnung der freien Stunden
        free_hours = max_arbeitszeit - total_hours

        # Debugging: Ergebnisse ausgeben
        print(f"Berechnung für Mitarbeiter: {mitarbeiter}")
        print(f"Maximale Arbeitszeit: {max_arbeitszeit}")
        print(f"Total Stunden pro Woche: {total_hours}")
        print(f"Freie Stunden: {free_hours}")

        # Rückgabe der Ergebnisse als Dictionary
        return {"total_hours": total_hours, "free_hours": free_hours}


class VollzeitaequivalentStunden(models.Model):
    wert = models.IntegerField()

    def __str__(self):
        return str(self.wert)

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:vollzeitaequivalentstunden_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:vollzeitaequivalentstunden_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:vollzeitaequivalentstunden_delete', args=[str(self.id)])





