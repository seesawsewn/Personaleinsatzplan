from django import forms
from .models import (Auftrag, Personaleinsatzplan, Betreuungsschluessel, Mitarbeiter, MitarbeiterBetreuungsschluessel,
                     Niederlassung, Position)
from datetime import datetime

class PersonaleinsatzplanForm(forms.ModelForm):
    MONATS_CHOICES = [
        (1, 'Januar'), (2, 'Februar'), (3, 'März'), (4, 'April'),
        (5, 'Mai'), (6, 'Juni'), (7, 'Juli'), (8, 'August'),
        (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Dezember')
    ]

    gueltigkeit_monat = forms.ChoiceField(
        choices=MONATS_CHOICES,
        label="Monat",
        widget=forms.Select(attrs={'placeholder': 'Monat der Gültigkeit'})
    )
    gueltigkeit_jahr = forms.IntegerField(
        label="Jahr",
        min_value=datetime.now().year - 2,  # Maximal zwei Jahre zurück
        max_value=datetime.now().year + 10,  # Maximal 10 Jahre in die Zukunft
        widget=forms.NumberInput(attrs={'placeholder': 'Jahr der Gültigkeit'})
    )

    class Meta:
        model = Personaleinsatzplan
        fields = ['gueltigkeit_monat', 'gueltigkeit_jahr', 'kostentraeger', 'ersteller', 'status', 'niederlassung']

        widgets = {
            'kostentraeger': forms.TextInput(attrs={'placeholder': 'Kostenträger'}),
            'ersteller': forms.TextInput(attrs={'placeholder': 'Ersteller:in'}),
            'status': forms.Select(attrs={'placeholder': 'Status auswählen'}),
            'niederlassung': forms.Select(attrs={'placeholder': 'Niederlassung auswählen'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        monat = int(cleaned_data.get('gueltigkeit_monat', 0))
        jahr = int(cleaned_data.get('gueltigkeit_jahr', 0))

        # Prüfung: Jahr darf nicht außerhalb der erlaubten Zeitspanne liegen
        aktuelles_datum = datetime.now()
        min_jahr = aktuelles_datum.year - 2
        max_jahr = aktuelles_datum.year + 10

        if jahr < min_jahr or jahr > max_jahr:
            self.add_error('gueltigkeit_jahr', f"Das Jahr muss zwischen {min_jahr} und {max_jahr} liegen.")

        return cleaned_data



class AuftragForm(forms.ModelForm):
    startdatum = forms.DateField(
        label="Startdatum",
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'tt.mm.jjjj'}),
        input_formats=['%d.%m.%Y']
    )
    enddatum = forms.DateField(
        label="Enddatum",
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'tt.mm.jjjj'}),
        input_formats=['%d.%m.%Y']
    )
    vergabenummer = forms.CharField(
        label="Vergabenummer",
        widget=forms.TextInput(attrs={'placeholder': '(z.B. 901-19-45ind-71274 / Los 1)'})
    )
    optionsnummer = forms.CharField(
        label="Optionsnummer",
        widget=forms.TextInput(attrs={'placeholder': 'z.B. 2. Option lfd. Nr. 1'})
    )
    massnahmenummer = forms.CharField(
        label="Maßnahmenummer",
        widget=forms.TextInput(attrs={'placeholder': 'z.B. 955/99/22'})
    )
    max_klienten = forms.IntegerField(
        label="Maximale Klienten",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Maximalanzahl Teilnehmer:innen'})
    )
    mindest_klienten = forms.IntegerField(
        label="Mindestanzahl Klienten",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Mindestanzahl Teilnehmer:innen'})
    )
    aktuell_klienten = forms.IntegerField(
        label="Aktuelle Klienten",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Aktuelle Anzahl Teilnehmer:innen'})
    )

    class Meta:
        model = Auftrag
        fields = [
            'name', 'vergabenummer', 'optionsnummer', 'massnahmenummer', 'startdatum', 'enddatum',
            'max_klienten', 'mindest_klienten', 'aktuell_klienten', 'personaleinsatzplan'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Projektname'}),
            'personaleinsatzplan': forms.Select(attrs={'placeholder': 'Personaleinsatzplan auswählen'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Zusätzliche Validierung oder Anpassungen können hier hinzugefügt werden

    def clean(self):
        cleaned_data = super().clean()
        startdatum = cleaned_data.get('startdatum')
        enddatum = cleaned_data.get('enddatum')

        # Prüfung: Enddatum muss nach dem Startdatum liegen
        if startdatum and enddatum and startdatum > enddatum:
            self.add_error('enddatum', "Das Enddatum muss nach dem Startdatum liegen.")

        # Prüfung: Mindestanzahl Klienten darf nicht größer als maximale Klientenanzahl sein
        max_klienten = cleaned_data.get('max_klienten')
        mindest_klienten = cleaned_data.get('mindest_klienten')

        if max_klienten is not None and mindest_klienten is not None and mindest_klienten > max_klienten:
            self.add_error('mindest_klienten', "Die Mindestanzahl Klienten darf nicht größer als die maximale Klientenanzahl sein.")

        return cleaned_data




class BetreuungsschluesselForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label="Position",
        widget=forms.Select(attrs={'placeholder': 'Position auswählen'})
    )
    klienten_pro_betreuer = forms.IntegerField(
        label="Klienten pro Betreuer:in",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'z.B.: 8'})
    )
    auftrag = forms.ModelChoiceField(
        queryset=Auftrag.objects.all(),
        label="Auftrag",
        widget=forms.Select(attrs={'placeholder': 'Auftrag auswählen'})
    )

    class Meta:
        model = Betreuungsschluessel
        fields = ['position', 'klienten_pro_betreuer', 'auftrag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamisches Anpassen des Auftrags-Querysets (z. B. abhängig von Benutzer oder Kontext)
        if 'auftrag' in self.fields:
            self.fields['auftrag'].queryset = Auftrag.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        klienten_pro_betreuer = cleaned_data.get('klienten_pro_betreuer')
        auftrag = cleaned_data.get('auftrag')

        # Prüfung: Klienten pro Betreuer darf nicht null oder negativ sein
        if klienten_pro_betreuer is not None and klienten_pro_betreuer <= 0:
            self.add_error('klienten_pro_betreuer', "Die Anzahl der Klienten pro Betreuer:in muss größer als 0 sein.")

        # Prüfung: Auftrag muss gültig sein
        if auftrag is None:
            self.add_error('auftrag', "Ein gültiger Auftrag muss ausgewählt werden.")

        return cleaned_data



class MitarbeiterForm(forms.ModelForm):
    vorname = forms.CharField(
        label="Vorname",
        widget=forms.TextInput(attrs={'placeholder': 'Vorname der Mitarbeiter:in'})
    )
    nachname = forms.CharField(
        label="Nachname",
        widget=forms.TextInput(attrs={'placeholder': 'Nachname der Mitarbeiter:in'})
    )
    qualifikation = forms.CharField(
        label="Qualifikation",
        widget=forms.TextInput(attrs={'placeholder': 'z. B. Sozialarbeiter:in'})
    )
    max_woechentliche_arbeitszeit = forms.IntegerField(
        label="Wöchentliche Arbeitszeit",
        min_value=1,
        max_value=40,
        widget=forms.NumberInput(attrs={'placeholder': 'z. B. 39'})
    )
    personalnummer = forms.IntegerField(
        label="Personalnummer",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Eindeutige Personalnummer'})
    )
    geburtsdatum = forms.DateField(
        label="Geburtsdatum",
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'tt.mm.jjjj'}),
        input_formats=['%d.%m.%Y']
    )
    vertragsbeginn = forms.DateField(
        label="Vertragsbeginn",
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'tt.mm.jjjj'}),
        input_formats=['%d.%m.%Y']
    )
    vertragsendeBefristet = forms.DateField(
        label="Vertragsende (falls befristet)",
        required=False,
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'placeholder': 'tt.mm.jjjj'}),
        input_formats=['%d.%m.%Y']
    )
    unbefristet = forms.BooleanField(
        label="Unbefristeter Vertrag",
        required=False,
        widget=forms.CheckboxInput()
    )
    niederlassung = forms.ModelChoiceField(
        queryset=Niederlassung.objects.all(),
        label="Niederlassung",
        widget=forms.Select(attrs={'placeholder': 'Niederlassung auswählen'})
    )

    class Meta:
        model = Mitarbeiter
        fields = [
            'vorname', 'nachname', 'qualifikation', 'max_woechentliche_arbeitszeit',
            'personalnummer', 'geburtsdatum', 'vertragsbeginn', 'vertragsendeBefristet',
            'unbefristet', 'niederlassung'
        ]

    def clean(self):
        cleaned_data = super().clean()
        vertragsbeginn = cleaned_data.get('vertragsbeginn')
        vertragsendeBefristet = cleaned_data.get('vertragsendeBefristet')
        unbefristet = cleaned_data.get('unbefristet')

        # Prüfung: Vertragsende darf nicht vor Vertragsbeginn liegen
        if vertragsbeginn and vertragsendeBefristet and vertragsendeBefristet < vertragsbeginn:
            self.add_error('vertragsendeBefristet', "Das Vertragsende darf nicht vor dem Vertragsbeginn liegen.")

        # Prüfung: Befristet und unbefristet gleichzeitig prüfen
        if unbefristet and vertragsendeBefristet:
            self.add_error('unbefristet', "Ein Vertrag kann nicht unbefristet sein, wenn ein Vertragsende angegeben ist.")

        return cleaned_data




class MitarbeiterZuweisungForm(forms.ModelForm):
    mitarbeiter = forms.ModelChoiceField(
        queryset=Mitarbeiter.objects.none(),  # Leeres Queryset, wird dynamisch angepasst
        label="Mitarbeiter auswählen",
        widget=forms.Select(attrs={'placeholder': 'Mitarbeiter auswählen'})
    )
    anteil_stunden_pro_woche = forms.FloatField(
        label="Stundenanteil pro Woche im Projekt",
        widget=forms.NumberInput(attrs={'placeholder': 'z.B.: 39'})
    )
    kommentar = forms.CharField(
        label="Kommentar",
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'z.B.: hilf aus', 'rows': 1})
    )

    class Meta:
        model = MitarbeiterBetreuungsschluessel
        fields = ['mitarbeiter', 'anteil_stunden_pro_woche', 'kommentar']

    def __init__(self, *args, **kwargs):
        self.schluessel = kwargs.pop('schluessel', None)
        self.personaleinsatzplan = kwargs.pop('personaleinsatzplan', None)  # Der relevante Zeitraum
        super().__init__(*args, **kwargs)

        # Falls ein Betreuungsschlüssel angegeben ist, passe das Queryset an
        if self.schluessel:
            self.fields['mitarbeiter'].queryset = Mitarbeiter.objects.all()

        # Passe das Label für die Mitarbeiter dynamisch an
        self.fields['mitarbeiter'].label_from_instance = self._mitarbeiter_label

    def _mitarbeiter_label(self, obj):
        # Berechne total_hours und free_hours für den Mitarbeiter
        result = MitarbeiterBetreuungsschluessel.calculate_hours_and_free_time(obj, self.personaleinsatzplan)
        total_hours = result['total_hours']
        free_hours = result['free_hours']

        # Label mit Vorname, Nachname, total_hours und free_hours
        return f"{obj.vorname} {obj.nachname} (Total: {total_hours} Stunden, Frei: {free_hours} Stunden)"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.schluessel:
            instance.schluessel = self.schluessel
            instance.position = self.schluessel.position  # Position automatisch setzen
        if commit:
            instance.save()
        return instance
