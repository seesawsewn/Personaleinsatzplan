from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from PersonaleinsatzplanHaeH.models import Niederlassung, Personaleinsatzplan, Auftrag, Betreuungsschluessel, Mitarbeiter
from datetime import date


class StartseiteViewTests(TestCase):
    def setUp(self):
        """Erstelle Testdaten für die Startseite."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.client.login(username="testuser", password="password")

    def test_startseite_view(self):
        """Testet, ob die Startseite geladen wird."""
        response = self.client.get(reverse("PersonaleinsatzplanHaeH:startseite"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "startseite.html")
        self.assertIn("niederlassungen", response.context)
        self.assertEqual(len(response.context["niederlassungen"]), 1)


class PersonaleinsatzplanViewTests(TestCase):
    def setUp(self):
        """Setzt Testdaten für Personaleinsatzplan-Views auf."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.plan = Personaleinsatzplan.objects.create(
            gueltigkeit_monat=1,
            gueltigkeit_jahr=2025,
            kostentraeger="Kostentraeger ABC",
            ersteller="Admin",
            status="entwurf",
            niederlassung=self.niederlassung
        )
        self.client.login(username="testuser", password="password")

    def test_personaleinsatzplan_list_view(self):
        """Testet, ob die Liste aller Personaleinsatzpläne geladen wird."""
        response = self.client.get(reverse("PersonaleinsatzplanHaeH:personaleinsatzplan_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "personaleinsatzplan_list2.html")
        self.assertIn("personaleinsatzplaene", response.context)
        self.assertEqual(len(response.context["personaleinsatzplaene"]), 1)

    def test_personaleinsatzplan_detail_view(self):
        """Testet, ob die Detailansicht eines Personaleinsatzplans geladen wird."""
        response = self.client.get(reverse("PersonaleinsatzplanHaeH:personaleinsatzplan_detail", args=[self.plan.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "personaleinsatzplan_detail2.html")
        self.assertEqual(response.context["personaleinsatzplan"], self.plan)

    def test_personaleinsatzplan_create_view(self):
        """Testet das Erstellen eines neuen Personaleinsatzplans."""
        response = self.client.post(reverse("PersonaleinsatzplanHaeH:personaleinsatzplan_create"), {
            "gueltigkeit_monat": 2,
            "gueltigkeit_jahr": 2026,
            "kostentraeger": "Neuer Kostentraeger",
            "ersteller": "Tester",
            "status": "entwurf",
            "niederlassung": self.niederlassung.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect nach Erfolg
        self.assertEqual(Personaleinsatzplan.objects.count(), 2)

    def test_personaleinsatzplan_delete_view(self):
        """Testet das Löschen eines Personaleinsatzplans."""
        response = self.client.post(reverse("PersonaleinsatzplanHaeH:personaleinsatzplan_delete", args=[self.plan.id]))
        self.assertEqual(response.status_code, 302)  # Erfolgreiche Weiterleitung nach dem Löschen
        self.assertEqual(Personaleinsatzplan.objects.count(), 0)


class AuftragViewTests(TestCase):
    def setUp(self):
        """Setzt Testdaten für die Auftrag-Views auf."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.plan = Personaleinsatzplan.objects.create(
            gueltigkeit_monat=1,
            gueltigkeit_jahr=2025,
            kostentraeger="Kostentraeger ABC",
            ersteller="Admin",
            status="entwurf",
            niederlassung=self.niederlassung
        )
        self.auftrag = Auftrag.objects.create(
            name="Test Auftrag",
            vergabenummer="12345",
            optionsnummer="67890",
            massnahmenummer="54321",
            startdatum=date(2025, 1, 1),
            enddatum=date(2025, 12, 31),
            max_klienten=10,
            mindest_klienten=5,
            aktuell_klienten=7,
            personaleinsatzplan=self.plan
        )
        self.client.login(username="testuser", password="password")

    def test_auftrag_list_view(self):
        """Testet die Liste der Aufträge."""
        response = self.client.get(reverse("PersonaleinsatzplanHaeH:auftrag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auftrag_list.html")
        self.assertEqual(len(response.context["auftraege"]), 1)

    def test_auftrag_detail_view(self):
        """Testet die Detailansicht eines Auftrags."""
        response = self.client.get(reverse("PersonaleinsatzplanHaeH:auftrag_detail", args=[self.auftrag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auftrag_detail.html")
        self.assertEqual(response.context["auftrag"], self.auftrag)

    def test_auftrag_create_view(self):
        """Testet das Erstellen eines neuen Auftrags."""
        response = self.client.post(reverse("PersonaleinsatzplanHaeH:auftrag_create"), {
            "name": "Neuer Auftrag",
            "vergabenummer": "99999",
            "optionsnummer": "88888",
            "massnahmenummer": "77777",
            "startdatum": "01.01.2024",
            "enddatum": "02.01.2024",
            "max_klienten": 15,
            "mindest_klienten": 10,
            "aktuell_klienten": 12,
            "personaleinsatzplan": self.plan.id
        })
        print(response.context["form"].errors)  # Zeigt eventuelle Fehler im Formular an

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Auftrag.objects.count(), 2)

    def test_auftrag_delete_view(self):
        """Testet das Löschen eines Auftrags."""
        response = self.client.post(reverse("PersonaleinsatzplanHaeH:auftrag_delete", args=[self.auftrag.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Auftrag.objects.count(), 0)


class BetreuungsschluesselViewTests(TestCase):
    def setUp(self):
        """Setzt Testdaten für Betreuungsschlüssel-Views auf."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.niederlassung = Niederlassung.objects.create(name="Berlin")
        self.plan = Personaleinsatzplan.objects.create(
            gueltigkeit_monat=1,
            gueltigkeit_jahr=2025,
            kostentraeger="Kostentraeger ABC",
            ersteller="Admin",
            status="entwurf",
            niederlassung=self.niederlassung
        )
        self.auftrag = Auftrag.objects.create(
            name="Test Auftrag",
            vergabenummer="12345",
            optionsnummer="67890",
            massnahmenummer="54321",
            startdatum=date(2025, 1, 1),
            enddatum=date(2025, 12, 31),
            max_klienten=10,
            mindest_klienten=5,
            aktuell_klienten=7,
            personaleinsatzplan=self.plan
        )
        self.client.login(username="testuser", password="password")

    def test_betreuungsschluessel_create_view(self):
        """Testet das Erstellen eines Betreuungsschlüssels."""
        response = self.client.post(reverse("PersonaleinsatzplanHaeH:betreuungsschluessel_create"), {
            "name": "Test Betreuungsschlüssel",
            "klienten_pro_betreuer": 5,
            "auftrag": self.auftrag.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Betreuungsschluessel.objects.count(), 1)
