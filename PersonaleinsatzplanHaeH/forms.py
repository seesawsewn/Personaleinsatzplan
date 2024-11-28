from django import forms
from django.db.models import Sum
from .models import (Auftrag, Personaleinsatzplan, Betreuungsschluessel, Mitarbeiter, Niederlassung, Position,
                     PersonaleinsatzplanStatus, MitarbeiterBetreuungsschluessel, VollzeitaequivalentStunden)


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
    total_hours = forms.FloatField(disabled=True, label="Zugewiesene Stunden", required=False)
    freie_stunden = forms.FloatField(disabled=True, label="Freie Stunden", required=False)

    class Meta:
        model = MitarbeiterBetreuungsschluessel
        fields = ['mitarbeiter', 'anteil_stunden_pro_woche', 'kommentar', 'position', 'schluessel', 'auftrag']
        widgets = {
            'position': forms.HiddenInput(),
            'schluessel': forms.HiddenInput(),
            'auftrag': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.mitarbeiter:
            self.fields['total_hours'].initial = self.instance.total_hours
            self.fields['freie_stunden'].initial = self.instance.freie_stunden


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

            # Mitarbeiter mit noch verfügbaren freien Stunden
            zugewiesene_stunden = MitarbeiterBetreuungsschluessel.objects.values('mitarbeiter').annotate(
                total=Sum('zugewiesene_stunden')
            )
            freie_mitarbeiter_ids = [
                mitarbeiter['mitarbeiter'] for mitarbeiter in zugewiesene_stunden
                if mitarbeiter['total'] < Mitarbeiter.objects.get(
                    id=mitarbeiter['mitarbeiter']).max_woechentliche_arbeitszeit
            ]
            self.fields['mitarbeiter'].queryset = Mitarbeiter.objects.filter(id__in=freie_mitarbeiter_ids)

            self.fields['mitarbeiter'].label_from_instance = lambda obj: f"{obj.vorname} {obj.nachname} (Frei: {obj.max_woechentliche_arbeitszeit - MitarbeiterBetreuungsschluessel.objects.filter(mitarbeiter=obj).aggregate(total=Sum('zugewiesene_stunden'))['total'] or 0})"


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.schluessel:
            instance.schluessel = self.schluessel
            instance.position = self.schluessel.position  # Position automatisch setzen
        if commit:
            instance.save()
        return instance
