from django.test import TestCase
from PersonaleinsatzplanHaeH.models import Mitarbeiter, Personaleinsatzplan, Auftrag, Betreuungsschluessel, Niederlassung, Position
from datetime import date

class MitarbeiterModelTests(TestCase):
    def setUp(self):
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.mitarbeiter = Mitarbeiter.objects.create(
            vorname="Max",
            nachname="Mustermann",
            qualifikation="Ingenieur",
            max_woechentliche_arbeitszeit=40,
            personalnummer=123456,
            geburtsdatum=date(1990, 1, 1),
            vertragsbeginn=date(2020, 1, 1),
            niederlassung=self.niederlassung
        )

    def test_mitarbeiter_creation(self):
        """Testet, ob ein Mitarbeiter korrekt erstellt wird."""
        self.assertEqual(self.mitarbeiter.vorname, "Max")
        self.assertEqual(self.mitarbeiter.nachname, "Mustermann")
        self.assertEqual(self.mitarbeiter.qualifikation, "Ingenieur")

    def test_mitarbeiter_str(self):
        """Testet die __str__-Methode des Mitarbeiters"""
        self.assertEqual(str(self.mitarbeiter), "Max Mustermann")

    def test_get_absolute_url(self):
        """Testet, ob die get_absolute_url-Methode die richtige URL zurückgibt."""
        self.assertEqual(self.mitarbeiter.get_absolute_url(), f"/PersonaleinsatzplanHaeH/mitarbeiter/{self.mitarbeiter.id}/")


class PersonaleinsatzplanModelTests(TestCase):
    def setUp(self):
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.plan = Personaleinsatzplan.objects.create(
            gueltigkeit_monat=1,
            gueltigkeit_jahr=2025,
            kostentraeger="Kostentraeger ABC",
            ersteller="Admin",
            status="entwurf",
            niederlassung=self.niederlassung
        )

    def test_save_method_generates_correct_name(self):
        """Testet, ob die save-Methode den Namen korrekt generiert."""
        self.plan.save()
        self.assertEqual(self.plan.name, "Personaleinsatzplan Berlin - Januar 2025")

    def test_personaleinsatzplan_str(self):
        """Testet die __str__-Methode des Personaleinsatzplans."""
        self.assertEqual(str(self.plan), "Personaleinsatzplan Berlin - Januar 2025")


class AuftragModelTests(TestCase):
    def setUp(self):
        self.plan = Personaleinsatzplan.objects.create(
            gueltigkeit_monat=3,
            gueltigkeit_jahr=2025,
            kostentraeger="Kostentraeger XYZ",
            ersteller="Admin",
            status="entwurf",
            niederlassung=Niederlassung.objects.create(name="Hamburg")
        )

        self.auftrag = Auftrag.objects.create(
            name="Auftrag 1",
            vergabenummer="123",
            optionsnummer="456",
            massnahmenummer="789",
            startdatum=date(2025, 3, 1),
            enddatum=date(2025, 12, 31),
            max_klienten=20,
            mindest_klienten=10,
            aktuell_klienten=15,
            personaleinsatzplan=self.plan
        )

    def test_auftrag_creation(self):
        """Testet, ob ein Auftrag korrekt erstellt wird."""
        self.assertEqual(self.auftrag.name, "Auftrag 1")
        self.assertEqual(self.auftrag.vergabenummer, "123")
        self.assertEqual(self.auftrag.max_klienten, 20)

    def test_auftrag_str(self):
        """Testet die __str__-Methode des Auftrags."""
        self.assertEqual(str(self.auftrag), "Auftrag 1")


class BetreuungsschluesselModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(bezeichnung="Betreuer")
        self.auftrag = Auftrag.objects.create(
            name="Auftrag 1",
            vergabenummer="123",
            optionsnummer="456",
            massnahmenummer="789",
            startdatum=date(2025, 1, 1),
            enddatum=date(2025, 12, 31),
            max_klienten=20,
            mindest_klienten=10,
            aktuell_klienten=15,
            personaleinsatzplan=Personaleinsatzplan.objects.create(
                gueltigkeit_monat=1,
                gueltigkeit_jahr=2025,
                kostentraeger="Kostentraeger ABC",
                ersteller="Admin",
                status="entwurf",
                niederlassung=Niederlassung.objects.create(name="Berlin")
            )
        )
        self.schluessel = Betreuungsschluessel.objects.create(
            name="Standard",
            position=self.position,
            klienten_pro_betreuer=5,
            auftrag=self.auftrag
        )

    def test_benoetigte_VZA_max(self):
        """Testet, ob die benötigte VZA für maximale Klienten korrekt berechnet wird."""
        self.assertEqual(self.schluessel.benoetigte_VZA_max, 4.0)

    def test_benoetigte_VZA_aktuell(self):
        """Testet, ob die benötigte VZA für aktuelle Klienten korrekt berechnet wird."""
        self.assertEqual(self.schluessel.benoetigte_VZA_aktuell, 3.0)

    def test_betreuungsschluessel_str(self):
        """Testet die __str__-Methode des Betreuungsschlüssels."""
        self.assertEqual(str(self.schluessel), "Standard")
