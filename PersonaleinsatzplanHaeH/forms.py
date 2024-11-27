from django import forms
from .models import (Auftrag, Personaleinsatzplan, Betreuungsschluessel, Mitarbeiter, Niederlassung, Position,
                     PersonaleinsatzplanStatus, MitarbeiterBetreuungsschluessel, VollzeitaequivalentStunden,
                     MitarbeiterBerechnungen)

# Formular zum Erstellen und Bearbeiten eines Personaleinsatzplans
class PersonaleinsatzplanForm(forms.ModelForm):
    MONATS_CHOICES = [
        (1, 'Januar'), (2, 'Februar'), (3, 'März'), (4, 'April'),
        (5, 'Mai'), (6, 'Juni'), (7, 'Juli'), (8, 'August'),
        (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Dezember')
    ]

    gueltigkeit_monat = forms.ChoiceField(choices=MONATS_CHOICES, label="Monat")
    gueltigkeit_jahr = forms.IntegerField(label="Jahr", min_value=1900, max_value=2100, widget=forms.NumberInput(attrs={'placeholder': 'Jahr'}))

    class Meta:
        model = Personaleinsatzplan
        fields = ['name', 'gueltigkeit_monat', 'gueltigkeit_jahr', 'kostentraeger', 'ersteller', 'version', 'status', 'niederlassung']

# Formular zum Erstellen und Bearbeiten eines Auftrags
class AuftragForm(forms.ModelForm):
    class Meta:
        model = Auftrag
        fields = [
            'name', 'vergabenummer', 'optionsnummer', 'massnahmenummer', 'startdatum', 'enddatum',
            'max_klienten', 'mindest_klienten', 'aktuell_klienten', 'personaleinsatzplan'
        ]

# Formular zum Erstellen und Bearbeiten eines Betreuungsschlüssels
class BetreuungsschluesselForm(forms.ModelForm):
    class Meta:
        model = Betreuungsschluessel
        fields = ['name', 'position', 'klienten_pro_betreuer', 'auftrag']

# Formular zum Erstellen und Bearbeiten eines Mitarbeiters
class MitarbeiterForm(forms.ModelForm):
    class Meta:
        model = Mitarbeiter
        fields = ['vorname', 'nachname', 'qualifikation', 'max_woechentliche_arbeitszeit', 'personalnummer', 'geburtsdatum', 'vertragsbeginn', 'vertragsendeBefristet', 'unbefristet', 'niederlassung']

class MitarbeiterBetreuungsschluesselForm(forms.ModelForm):
    class Meta:
        model = MitarbeiterBetreuungsschluessel
        fields = ['mitarbeiter', 'anteil_stunden_pro_woche', 'kommentar', 'position', 'schluessel', 'auftrag']
        widgets = {
            'position': forms.HiddenInput(),
            'schluessel': forms.HiddenInput(),
            'auftrag': forms.HiddenInput(),
        }

class NiederlassungForm(forms.ModelForm):
    class Meta:
        model = Niederlassung
        fields = ['name']

# Formular zum Erstellen und Bearbeiten einer Position
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['bezeichnung']

# Kann gelöscht werden
class PersonaleinsatzplanStatusForm(forms.ModelForm):
    class Meta:
        model = PersonaleinsatzplanStatus
        fields = ['name']

# Formular zum Erstellen und Bearbeiten eines VollzeitaequivalentStunden
class VollzeitaequivalentStundenForm(forms.ModelForm):
    class Meta:
        model = VollzeitaequivalentStunden
        fields = ['wert']

# Formular zur Zuweisung von Mitarbeitern zu einem Betreuungsschlüssel
class MitarbeiterZuweisungForm(forms.ModelForm):
    class Meta:
        model = MitarbeiterBetreuungsschluessel
        fields = ['mitarbeiter', 'anteil_stunden_pro_woche', 'kommentar']

    def __init__(self, *args, **kwargs):
        self.schluessel = kwargs.pop('schluessel', None)
        super().__init__(*args, **kwargs)

        if self.schluessel:
            zugewiesene_mitarbeiter = MitarbeiterBetreuungsschluessel.objects.filter(
                schluessel=self.schluessel).values_list('mitarbeiter', flat=True)
            self.fields['mitarbeiter'].queryset = Mitarbeiter.objects.exclude(id__in=zugewiesene_mitarbeiter)

            self.fields['mitarbeiter'].label_from_instance = lambda obj: MitarbeiterBerechnungen.mitarbeiter_label_with_differenz(obj)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.schluessel:
            instance.schluessel = self.schluessel
            instance.position = self.schluessel.position  # Position automatisch setzen
        if commit:
            instance.save()
        return instance
