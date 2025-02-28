from django.test import TestCase
from datetime import datetime, timedelta
from PersonaleinsatzplanHaeH.forms import (
    PersonaleinsatzplanForm, AuftragForm, BetreuungsschluesselForm, MitarbeiterForm, MitarbeiterZuweisungForm
)
from PersonaleinsatzplanHaeH.models import (
    Personaleinsatzplan, Auftrag, Betreuungsschluessel, Mitarbeiter, Niederlassung, Position
)


class PersonaleinsatzplanFormTests(TestCase):

    def setUp(self):
        """Erstellt eine Test-Niederlassung"""
        self.niederlassung = Niederlassung.objects.create(name="Test Niederlassung")

    def test_valid_personaleinsatzplan_form(self):
        """Testet, ob ein gültiges Formular ohne Fehler validiert wird"""
        form_data = {
            "gueltigkeit_monat": 1,
            "gueltigkeit_jahr": datetime.now().year,
            "kostentraeger": "Test Kostenträger",
            "ersteller": "Max Mustermann",
            "status": "Aktiv",
            "niederlassung": self.niederlassung.id
        }
        form = PersonaleinsatzplanForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_in_personaleinsatzplan_form(self):
        """Testet, ob eine ungültige Jahreszahl abgefangen wird"""
        form_data = {
            "gueltigkeit_monat": 1,
            "gueltigkeit_jahr": datetime.now().year - 3,  # Zu weit in der Vergangenheit
            "kostentraeger": "Test Kostenträger",
            "ersteller": "Max Mustermann",
            "status": "Aktiv",
            "niederlassung": self.niederlassung.id
        }
        form = PersonaleinsatzplanForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("gueltigkeit_jahr", form.errors)


class AuftragFormTests(TestCase):

    def setUp(self):
        """Erstellt einen Test-Personaleinsatzplan"""
        self.niederlassung = Niederlassung.objects.create(name="Test Niederlassung")
        self.personaleinsatzplan = Personaleinsatzplan.objects.create(
            name="Testplan",
            gueltigkeit_monat=1,
            gueltigkeit_jahr=datetime.now().year,
            kostentraeger="Test Kostenträger",
            ersteller="Test Ersteller",
            niederlassung=self.niederlassung
        )

    def test_valid_auftrag_form(self):
        """Testet, ob ein gültiger Auftrag erstellt werden kann"""
        form_data = {
            "name": "Test Auftrag",
            "vergabenummer": "12345",
            "optionsnummer": "54321",
            "massnahmenummer": "99999",
            "startdatum": (datetime.now()).strftime('%d.%m.%Y'),
            "enddatum": (datetime.now() + timedelta(days=10)).strftime('%d.%m.%Y'),
            "max_klienten": 10,
            "mindest_klienten": 5,
            "aktuell_klienten": 8,
            "personaleinsatzplan": self.personaleinsatzplan.id
        }
        form = AuftragForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_auftrag_form_dates(self):
        """Testet, ob das Enddatum vor dem Startdatum erkannt wird"""
        form_data = {
            "name": "Test Auftrag",
            "vergabenummer": "12345",
            "optionsnummer": "54321",
            "massnahmenummer": "99999",
            "startdatum": (datetime.now() + timedelta(days=10)).strftime('%d.%m.%Y'),
            "enddatum": (datetime.now()).strftime('%d.%m.%Y'),  # Falsche Reihenfolge
            "max_klienten": 10,
            "mindest_klienten": 5,
            "aktuell_klienten": 8,
            "personaleinsatzplan": self.personaleinsatzplan.id
        }
        form = AuftragForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("enddatum", form.errors)

    def test_invalid_auftrag_form_klienten(self):
        """Testet, ob die Mindest-Klienten-Anzahl nicht größer als die maximale Anzahl sein darf"""
        form_data = {
            "name": "Test Auftrag",
            "vergabenummer": "12345",
            "optionsnummer": "54321",
            "massnahmenummer": "99999",
            "startdatum": (datetime.now()).strftime('%d.%m.%Y'),
            "enddatum": (datetime.now() + timedelta(days=10)).strftime('%d.%m.%Y'),
            "max_klienten": 5,
            "mindest_klienten": 10,  # Fehler: Mindestzahl > Maximalzahl
            "aktuell_klienten": 3,
            "personaleinsatzplan": self.personaleinsatzplan.id
        }
        form = AuftragForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("mindest_klienten", form.errors)


class BetreuungsschluesselFormTests(TestCase):

    def setUp(self):
        """Erstellt eine Test-Position und einen Test-Auftrag"""
        self.position = Position.objects.create(bezeichnung="Test Position")
        self.niederlassung = Niederlassung.objects.create(name="Test Niederlassung")
        self.personaleinsatzplan = Personaleinsatzplan.objects.create(
            name="Testplan",
            gueltigkeit_monat=1,
            gueltigkeit_jahr=datetime.now().year,
            kostentraeger="Test Kostenträger",
            ersteller="Test Ersteller",
            niederlassung=self.niederlassung
        )
        self.auftrag = Auftrag.objects.create(
            name="Test Auftrag",
            vergabenummer="12345",
            optionsnummer="54321",
            massnahmenummer="99999",
            startdatum="2025-01-01",
            enddatum="2025-12-31",
            max_klienten=10,
            mindest_klienten=5,
            aktuell_klienten=8,
            personaleinsatzplan=self.personaleinsatzplan
        )

    def test_valid_betreuungsschluessel_form(self):
        """Testet, ob ein gültiges Betreuungsschlüssel-Formular funktioniert"""
        form_data = {
            "position": self.position.id,
            "klienten_pro_betreuer": 5,
            "auftrag": self.auftrag.id
        }
        form = BetreuungsschluesselForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_betreuungsschluessel_form(self):
        """Testet, ob `klienten_pro_betreuer` nicht null oder negativ sein darf"""
        form_data = {
            "position": self.position.id,
            "klienten_pro_betreuer": 0,  # Fehlerhafte Eingabe
            "auftrag": self.auftrag.id
        }
        form = BetreuungsschluesselForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("klienten_pro_betreuer", form.errors)


class MitarbeiterFormTests(TestCase):

    def setUp(self):
        """Erstellt eine Test-Niederlassung"""
        self.niederlassung = Niederlassung.objects.create(name="Test Niederlassung")

    def test_valid_mitarbeiter_form(self):
        """Testet, ob ein gültiges Mitarbeiter-Formular akzeptiert wird"""
        form_data = {
            "vorname": "Max",
            "nachname": "Mustermann",
            "qualifikation": "Sozialarbeiter",
            "max_woechentliche_arbeitszeit": 40,
            "personalnummer": 123456,
            "geburtsdatum": "1990-01-01",
            "vertragsbeginn": "2024-01-01",
            "unbefristet": True,
            "niederlassung": self.niederlassung.id
        }
        form = MitarbeiterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_mitarbeiter_form(self):
        """Testet, ob Vertragsende vor Vertragsbeginn erkannt wird"""
        form_data = {
            "vorname": "Max",
            "nachname": "Mustermann",
            "vertragsbeginn": "2025-01-01",
            "vertragsendeBefristet": "2024-01-01",  # Fehlerhafte Reihenfolge
            "niederlassung": self.niederlassung.id
        }
        form = MitarbeiterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("vertragsendeBefristet", form.errors)
