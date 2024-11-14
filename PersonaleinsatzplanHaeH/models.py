from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse


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
    niederlassung = models.ForeignKey(Niederlassung, on_delete=models.SET_NULL, null=True, blank=True)

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
    name = models.CharField(max_length=255)
    startdatum = models.DateField()
    enddatum = models.DateField()
    kostentraeger = models.CharField(max_length=255)
    ersteller = models.CharField(max_length=255)
    version = models.IntegerField()
    status = models.ForeignKey(PersonaleinsatzplanStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='personaleinsatzplaene')

    def __str__(self):
        return self.name

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
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    klienten_pro_betreuer = models.IntegerField()
    benoetigte_VZA_max = models.FloatField(default=0)
    benoetigte_VZA_mindest = models.FloatField(default=0)
    benoetigte_VZA_aktuell = models.FloatField(default=0)
    abgedeckte_VZA = models.FloatField(default=0, null=True)
    differenz_VZA_max = models.FloatField(null=True)
    differenz_VZA_mindest = models.FloatField(null=True)
    differenz_VZA_aktuell = models.FloatField(null=True)
    auftrag = models.ForeignKey(Auftrag, on_delete=models.CASCADE, related_name='betreuungsschluessel', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_delete', args=[str(self.id)])


class MitarbeiterBetreuungsschluessel(models.Model):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    anteil_stunden_pro_woche = models.FloatField()
    kommentar = models.TextField(blank=True, null=True)
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, null=True, blank=True, related_name='betreuungsschluessel_zuweisungen')
    schluessel = models.ForeignKey(Betreuungsschluessel, on_delete=models.SET_NULL, null=True, blank=True, related_name='mitarbeiter_zuweisungen')
    auftrag = models.ForeignKey(Auftrag, on_delete=models.SET_NULL, null=True, blank=True, related_name='mitarbeiter_betreuungsschluessel')

    def __str__(self):
        return f"{self.mitarbeiter} - {self.schluessel}"

    def get_absolute_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiterbetreuungsschluessel_delete', args=[str(self.id)])


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


class VZABerechnen:
    #@staticmethod
    #def berechne_aktuell_klienten(auftrag):
     #   if auftrag:
      #      return MitarbeiterBetreuungsschluessel.objects.filter(auftrag=auftrag).count()
       # return 0

    @staticmethod
    def berechne_abgedeckte_vza(schluessel_id):
        total_stunden = MitarbeiterBetreuungsschluessel.objects.filter(schluessel_id=schluessel_id).aggregate(
            total=models.Sum('anteil_stunden_pro_woche'))['total']
        vza_wert = VollzeitaequivalentStunden.objects.first().wert if VollzeitaequivalentStunden.objects.exists() else 1
        return (total_stunden / vza_wert) if total_stunden else 0

    @staticmethod
    def berechne_benoetigte_vza_max(schluessel):
        if schluessel.auftrag:
            return schluessel.auftrag.max_klienten / schluessel.klienten_pro_betreuer
        return 0

    @staticmethod
    def berechne_benoetigte_vza_mindest(schluessel):
        if schluessel.auftrag:
            return schluessel.auftrag.mindest_klienten / schluessel.klienten_pro_betreuer
        return 0

    @staticmethod
    def berechne_benoetigte_vza_aktuell(schluessel):
        if schluessel.auftrag:
            return schluessel.auftrag.aktuell_klienten / schluessel.klienten_pro_betreuer
        return 0

    @staticmethod
    def berechne_differenz_vza_max(schluessel):
        return schluessel.benoetigte_VZA_max - schluessel.abgedeckte_VZA

    @staticmethod
    def berechne_differenz_vza_mindest(schluessel):
        return schluessel.benoetigte_VZA_mindest - schluessel.abgedeckte_VZA

    @staticmethod
    def berechne_differenz_vza_aktuell(schluessel):
        return schluessel.benoetigte_VZA_aktuell - schluessel.abgedeckte_VZA

    @classmethod
    def aktualisiere_abgedeckte_vza(cls, schluessel):
        schluessel.abgedeckte_VZA = round(cls.berechne_abgedeckte_vza(schluessel.id), 1)
        schluessel.save()

    @classmethod
    def aktualisiere_benoetigte_vza_max(cls, schluessel):
        schluessel.benoetigte_VZA_max = cls.berechne_benoetigte_vza_max(schluessel)
        schluessel.save()

    @classmethod
    def aktualisiere_benoetigte_vza_mindest(cls, schluessel):
        schluessel.benoetigte_VZA_mindest = cls.berechne_benoetigte_vza_mindest(schluessel)
        schluessel.save()

    @classmethod
    def aktualisiere_benoetigte_vza_aktuell(cls, schluessel):
        schluessel.benoetigte_VZA_aktuell = cls.berechne_benoetigte_vza_aktuell(schluessel)
        schluessel.save()

    #@classmethod
    #def aktualisiere_aktuell_klienten(cls, auftrag):
     #   auftrag.aktuell_klienten = cls.berechne_aktuell_klienten(auftrag)
     #   auftrag.save()

    @classmethod
    def aktualisiere_differenz_vza_max(cls, schluessel):
        schluessel.differenz_VZA_max = cls.berechne_differenz_vza_max(schluessel)
        schluessel.save()

    @classmethod
    def aktualisiere_differenz_vza_mindest(cls, schluessel):
        schluessel.differenz_VZA_mindest = cls.berechne_differenz_vza_mindest(schluessel)
        schluessel.save()

    @classmethod
    def aktualisiere_differenz_vza_aktuell(cls, schluessel):
        schluessel.differenz_VZA_aktuell = cls.berechne_differenz_vza_aktuell(schluessel)
        schluessel.save()

    @classmethod
    def mitarbeiter_geaendert(cls, schluessel):
        cls.aktualisiere_abgedeckte_vza(schluessel)
        cls.aktualisiere_benoetigte_vza_max(schluessel)
        cls.aktualisiere_benoetigte_vza_mindest(schluessel)
        cls.aktualisiere_benoetigte_vza_aktuell(schluessel)
        cls.aktualisiere_differenz_vza_max(schluessel)
        cls.aktualisiere_differenz_vza_mindest(schluessel)
        cls.aktualisiere_differenz_vza_aktuell(schluessel)
        #if schluessel.auftrag:
            #cls.aktualisiere_aktuell_klienten(schluessel.auftrag)


@receiver(post_save, sender=MitarbeiterBetreuungsschluessel)
@receiver(post_delete, sender=MitarbeiterBetreuungsschluessel)
def mitarbeiter_geaendert_handler(sender, instance, **kwargs):
    if instance.schluessel:
        VZABerechnen.mitarbeiter_geaendert(instance.schluessel)

@receiver(post_save, sender=Auftrag)
def auftrag_geaendert_handler(sender, instance, **kwargs):
    for schluessel in instance.betreuungsschluessel.all():
        VZABerechnen.mitarbeiter_geaendert(schluessel)


from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mitarbeiter, MitarbeiterBetreuungsschluessel


class MitarbeiterBerechnungen:
    @staticmethod
    def berechne_gesamt_stunden_pro_woche(mitarbeiter):
        total_stunden = MitarbeiterBetreuungsschluessel.objects.filter(mitarbeiter=mitarbeiter).aggregate(
            total=Sum('anteil_stunden_pro_woche')
        )['total']

        return total_stunden if total_stunden else 0.0

    @staticmethod
    def berechne_differenz_max_arbeitszeit(mitarbeiter):

        gesamt_stunden = MitarbeiterBerechnungen.berechne_gesamt_stunden_pro_woche(mitarbeiter)
        differenz = mitarbeiter.max_woechentliche_arbeitszeit - gesamt_stunden

        return differenz

    @staticmethod
    def mitarbeiter_label_with_differenz(mitarbeiter):

        differenz = MitarbeiterBerechnungen.berechne_differenz_max_arbeitszeit(mitarbeiter)
        return f"{mitarbeiter.vorname} {mitarbeiter.nachname} (Verfügbare Stunden: {differenz:.1f})"


@receiver(post_save, sender=MitarbeiterBetreuungsschluessel)
@receiver(post_delete, sender=MitarbeiterBetreuungsschluessel)
def mitarbeiter_betreuungsschluessel_geaendert_handler(sender, instance, **kwargs):

    if instance.mitarbeiter:
        MitarbeiterBerechnungen.berechne_differenz_max_arbeitszeit(instance.mitarbeiter)
