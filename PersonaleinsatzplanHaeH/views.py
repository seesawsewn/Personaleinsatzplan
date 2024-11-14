from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Auftrag, Personaleinsatzplan, Betreuungsschluessel, Mitarbeiter, Niederlassung, Position, \
    PersonaleinsatzplanStatus, MitarbeiterBetreuungsschluessel, VollzeitaequivalentStunden, MitarbeiterBerechnungen
from django.shortcuts import redirect
from .forms import MitarbeiterZuweisungForm

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views import View


# Erstellen eines Personaleinsatzplans
class PersonaleinsatzplanCreateView(CreateView):
    model = Personaleinsatzplan
    fields = ['name', 'startdatum', 'enddatum', 'kostentraeger', 'ersteller', 'version', 'status']
    template_name = 'personaleinsatzplan_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:personaleinsatzplan_list')

# Liste aller Personaleinsatzpläne anzeigen
class PersonaleinsatzplanListView(ListView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_list.html'
    context_object_name = 'personaleinsatzplaene'

# Detailansicht eines Personaleinsatzplans
class PersonaleinsatzplanDetailView(DetailView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_detail.html'
    context_object_name = 'personaleinsatzplan'

# Aktualisieren eines Personaleinsatzplans
class PersonaleinsatzplanUpdateView(UpdateView):
    model = Personaleinsatzplan
    fields = ['name', 'startdatum', 'enddatum', 'kostentraeger', 'ersteller', 'version', 'status']
    template_name = 'personaleinsatzplan_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:personaleinsatzplan_list')

# Löschen eines Personaleinsatzplans
class PersonaleinsatzplanDeleteView(DeleteView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:personaleinsatzplan_list')

# Erstellen eines Auftrags
class AuftragCreateView(CreateView):
    model = Auftrag
    fields = [
        'name', 'vergabenummer', 'optionsnummer', 'massnahmenummer', 'startdatum', 'enddatum',
        'max_klienten', 'mindest_klienten', 'aktuell_klienten', 'personaleinsatzplan'
    ]
    template_name = 'auftrag_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:auftrag_list')

# Liste aller Aufträge anzeigen
class AuftragListView(ListView):
    model = Auftrag
    template_name = 'auftrag_list.html'
    context_object_name = 'auftraege'

# Detailansicht eines Auftrags
class AuftragDetailView(DetailView):
    model = Auftrag
    template_name = 'auftrag_detail.html'
    context_object_name = 'auftrag'

# Aktualisieren eines Auftrags
class AuftragUpdateView(UpdateView):
    model = Auftrag
    fields = [
        'name', 'vergabenummer', 'optionsnummer', 'massnahmenummer', 'startdatum', 'enddatum',
        'max_klienten', 'mindest_klienten', 'aktuell_klienten', 'personaleinsatzplan'
    ]
    template_name = 'auftrag_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:auftrag_list')

# Löschen eines Auftrags
class AuftragDeleteView(DeleteView):
    model = Auftrag
    template_name = 'auftrag_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:auftrag_list')

# Erstellen eines Betreuungsschlüssels
class BetreuungsschluesselCreateView(CreateView):
    model = Betreuungsschluessel
    fields = ['name', 'position', 'klienten_pro_betreuer', 'auftrag']
    template_name = 'betreuungsschluessel_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:betreuungsschluessel_list')

# Liste aller Betreuungsschlüssel anzeigen
class BetreuungsschluesselListView(ListView):
    model = Betreuungsschluessel
    template_name = 'betreuungsschluessel_list.html'
    context_object_name = 'betreuungsschluessel'

# Detailansicht eines Betreuungsschlüssels
class BetreuungsschluesselDetailView(DetailView, FormView):
    model = Betreuungsschluessel
    template_name = 'betreuungsschluessel_detail.html'
    context_object_name = 'betreuungsschluessel'
    form_class = MitarbeiterZuweisungForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zuweisung_form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['schluessel'] = self.object  # Betreuungsschlüssel an das Formular übergeben
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)

# Aktualisieren eines Betreuungsschlüssels
class BetreuungsschluesselUpdateView(UpdateView):
    model = Betreuungsschluessel
    fields = ['name', 'position', 'klienten_pro_betreuer', 'auftrag']
    template_name = 'betreuungsschluessel_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:betreuungsschluessel_list')

# Löschen eines Betreuungsschlüssels
class BetreuungsschluesselDeleteView(DeleteView):
    model = Betreuungsschluessel
    template_name = 'betreuungsschluessel_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:betreuungsschluessel_list')

# Erstellen eines Mitarbeiters
class MitarbeiterCreateView(CreateView):
    model = Mitarbeiter
    fields = ['vorname', 'nachname', 'qualifikation', 'max_woechentliche_arbeitszeit', 'personalnummer', 'geburtsdatum', 'vertragsbeginn', 'vertragsendeBefristet', 'unbefristet', 'niederlassung']
    template_name = 'mitarbeiter_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:mitarbeiter_list')

# Liste aller Mitarbeiter anzeigen
class MitarbeiterListView(ListView):
    model = Mitarbeiter
    template_name = 'mitarbeiter_list.html'
    context_object_name = 'mitarbeiter'


# Detailansicht eines Mitarbeiters
class MitarbeiterDetailView(DetailView):
    model = Mitarbeiter
    template_name = 'mitarbeiter_detail.html'
    context_object_name = 'mitarbeiter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mitarbeiter = self.object

        differenz_stunden = MitarbeiterBerechnungen.berechne_differenz_max_arbeitszeit(mitarbeiter)
        context['differenz_stunden'] = differenz_stunden

        betreuungsschluessel_zuweisungen = MitarbeiterBetreuungsschluessel.objects.filter(
            mitarbeiter=mitarbeiter).select_related('schluessel', 'auftrag')
        auftraege_info = []

        for zuweisung in betreuungsschluessel_zuweisungen:
            if zuweisung.schluessel and zuweisung.schluessel.auftrag:
                auftrag_info = {
                    'auftrag': zuweisung.schluessel.auftrag,
                    'anteil_stunden_pro_woche': zuweisung.anteil_stunden_pro_woche
                }
                auftraege_info.append(auftrag_info)

        context['auftraege_info'] = auftraege_info

        return context

# Aktualisieren eines Mitarbeiters
class MitarbeiterUpdateView(UpdateView):
    model = Mitarbeiter
    fields = ['vorname', 'nachname', 'qualifikation', 'max_woechentliche_arbeitszeit', 'personalnummer', 'geburtsdatum', 'vertragsbeginn', 'vertragsendeBefristet', 'unbefristet', 'niederlassung']
    template_name = 'mitarbeiter_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:mitarbeiter_list')

# Löschen eines Mitarbeiters
class MitarbeiterDeleteView(DeleteView):
    model = Mitarbeiter
    template_name = 'mitarbeiter_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:mitarbeiter_list')


class MitarbeiterBetreuungsschluesselCreateView(CreateView):
    model = MitarbeiterBetreuungsschluessel
    fields = ['position', 'anteil_stunden_pro_woche', 'kommentar', 'mitarbeiter', 'schluessel']
    template_name = 'mitarbeiter_betreuungsschluessel_form.html'
    success_url = reverse_lazy('mitarbeiter_betreuungsschluessel_list')

# Liste aller MitarbeiterBetreuungsschluessel anzeigen
class MitarbeiterBetreuungsschluesselListView(ListView):
    model = MitarbeiterBetreuungsschluessel
    template_name = 'mitarbeiter_betreuungsschluessel_list.html'
    context_object_name = 'mitarbeiter_betreuungsschluessel'

# Detailansicht eines MitarbeiterBetreuungsschluessel
class MitarbeiterBetreuungsschluesselDetailView(DetailView):
    model = MitarbeiterBetreuungsschluessel
    template_name = 'mitarbeiter_betreuungsschluessel_detail.html'
    context_object_name = 'mitarbeiter_betreuungsschluessel'

# Aktualisieren eines MitarbeiterBetreuungsschluessel
class MitarbeiterBetreuungsschluesselUpdateView(UpdateView):
    model = MitarbeiterBetreuungsschluessel
    fields = ['position', 'anteil_stunden_pro_woche', 'kommentar', 'mitarbeiter', 'schluessel']
    template_name = 'mitarbeiter_betreuungsschluessel_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:mitarbeiter_betreuungsschluessel_list')

# Löschen eines MitarbeiterBetreuungsschluessel
from django.urls import reverse_lazy

class MitarbeiterBetreuungsschluesselDeleteView(DeleteView):
    model = MitarbeiterBetreuungsschluessel
    template_name = 'mitarbeiter_betreuungsschluessel_confirm_delete.html'

    def get_success_url(self):
        # Erfolgs-URL: Nach dem Löschen wird zur Detailansicht des zugehörigen Betreuungsschlüssels weitergeleitet
        betreuungsschluessel = self.object.schluessel
        return reverse_lazy('PersonaleinsatzplanHaeH:betreuungsschluessel_detail', kwargs={'pk': betreuungsschluessel.pk})


# Erstellen einer Niederlassung
class NiederlassungCreateView(CreateView):
    model = Niederlassung
    fields = ['name']
    template_name = 'niederlassung_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:niederlassung_list')

# Liste aller Niederlassungen anzeigen
class NiederlassungListView(ListView):
    model = Niederlassung
    template_name = 'niederlassung_list.html'
    context_object_name = 'niederlassungen'

# Detailansicht einer Niederlassung
class NiederlassungDetailView(DetailView):
    model = Niederlassung
    template_name = 'niederlassung_detail.html'
    context_object_name = 'niederlassung'

# Aktualisieren einer Niederlassung
class NiederlassungUpdateView(UpdateView):
    model = Niederlassung
    fields = ['name']
    template_name = 'niederlassung_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:niederlassung_list')

# Löschen einer Niederlassung
class NiederlassungDeleteView(DeleteView):
    model = Niederlassung
    template_name = 'niederlassung_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:niederlassung_list')

# Erstellen einer Position
class PositionCreateView(CreateView):
    model = Position
    fields = ['bezeichnung']
    template_name = 'position_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:position_list')

# Liste aller Positionen anzeigen
class PositionListView(ListView):
    model = Position
    template_name = 'position_list.html'
    context_object_name = 'positionen'

# Detailansicht einer Position
class PositionDetailView(DetailView):
    model = Position
    template_name = 'position_detail.html'
    context_object_name = 'position'

# Aktualisieren einer Position
class PositionUpdateView(UpdateView):
    model = Position
    fields = ['bezeichnung']
    template_name = 'position_form.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:position_list')

# Löschen einer Position
class PositionDeleteView(DeleteView):
    model = Position
    template_name = 'position_confirm_delete.html'
    success_url = reverse_lazy('PersonaleinsatzplanHaeH:position_list')


class PersonaleinsatzplanStatusCreateView(CreateView):
    model = PersonaleinsatzplanStatus
    fields = ['name']
    template_name = 'personaleinsatzplanstatus_form.html'
    success_url = reverse_lazy('personaleinsatzplanstatus_list')

# Liste aller PersonaleinsatzplanStatus anzeigen
class PersonaleinsatzplanStatusListView(ListView):
    model = PersonaleinsatzplanStatus
    template_name = 'personaleinsatzplanstatus_list.html'
    context_object_name = 'personaleinsatzplanstatus'

# Detailansicht eines PersonaleinsatzplanStatus
class PersonaleinsatzplanStatusDetailView(DetailView):
    model = PersonaleinsatzplanStatus
    template_name = 'personaleinsatzplanstatus_detail.html'
    context_object_name = 'personaleinsatzplanstatus'

# Aktualisieren eines PersonaleinsatzplanStatus
class PersonaleinsatzplanStatusUpdateView(UpdateView):
    model = PersonaleinsatzplanStatus
    fields = ['name']
    template_name = 'personaleinsatzplanstatus_form.html'
    success_url = reverse_lazy('personaleinsatzplanstatus_list')

# Löschen eines PersonaleinsatzplanStatus
class PersonaleinsatzplanStatusDeleteView(DeleteView):
    model = PersonaleinsatzplanStatus
    template_name = 'personaleinsatzplanstatus_confirm_delete.html'
    success_url = reverse_lazy('personaleinsatzplanstatus_list')

# Erstellen eines VollzeitaequivalentStunden
class VollzeitaequivalentStundenCreateView(CreateView):
    model = VollzeitaequivalentStunden
    fields = ['wert']
    template_name = 'vollzeitaequivalentstunden_form.html'
    success_url = reverse_lazy('vollzeitaequivalentstunden_list')

# Liste aller VollzeitaequivalentStunden anzeigen
class VollzeitaequivalentStundenListView(ListView):
    model = VollzeitaequivalentStunden
    template_name = 'vollzeitaequivalentstunden_list.html'
    context_object_name = 'vollzeitaequivalentstunden'

# Detailansicht eines VollzeitaequivalentStunden
class VollzeitaequivalentStundenDetailView(DetailView):
    model = VollzeitaequivalentStunden
    template_name = 'vollzeitaequivalentstunden_detail.html'
    context_object_name = 'vollzeitaequivalentstunden'

# Aktualisieren eines VollzeitaequivalentStunden
class VollzeitaequivalentStundenUpdateView(UpdateView):
    model = VollzeitaequivalentStunden
    fields = ['wert']
    template_name = 'vollzeitaequivalentstunden_form.html'
    success_url = reverse_lazy('vollzeitaequivalentstunden_list')

# Löschen eines VollzeitaequivalentStunden
class VollzeitaequivalentStundenDeleteView(DeleteView):
    model = VollzeitaequivalentStunden
    template_name = 'vollzeitaequivalentstunden_confirm_delete.html'
    success_url = reverse_lazy('vollzeitaequivalentstunden_list')


from django.views.generic import DetailView
from .models import Personaleinsatzplan, Auftrag, Betreuungsschluessel


class Personaleinsatzplanuebersicht(DetailView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_uebersicht.html'
    context_object_name = 'personaleinsatzplan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personaleinsatzplan = self.object

        # Alle Aufträge des Personaleinsatzplans abrufen
        auftraege = Auftrag.objects.filter(personaleinsatzplan=personaleinsatzplan)

        auftrag_details = []

        for auftrag in auftraege:
            betreuungsschluessel_list = Betreuungsschluessel.objects.filter(auftrag=auftrag)
            betreuungsschluessel_details = []

            for schluessel in betreuungsschluessel_list:
                mitarbeiter_zuweisungen = schluessel.mitarbeiter_zuweisungen.all()
                mitarbeiter_list = [{'name': f"{m.mitarbeiter.vorname} {m.mitarbeiter.nachname}",
                                     'anteil_stunden': m.anteil_stunden_pro_woche} for m in mitarbeiter_zuweisungen]

                betreuungsschluessel_details.append({
                    'name': schluessel.name,
                    'position': schluessel.position,
                    'klienten_pro_betreuer': schluessel.klienten_pro_betreuer,
                    'mitarbeiter': mitarbeiter_list
                })

            auftrag_details.append({
                'auftrag': auftrag,
                'betreuungsschluessel': betreuungsschluessel_details
            })

        context['auftrag_details'] = auftrag_details
        return context


class PersonaleinsatzplanPDFView(View):
    def get(self, request, *args, **kwargs):
        personaleinsatzplan_id = self.kwargs.get('pk')
        personaleinsatzplan = Personaleinsatzplan.objects.get(pk=personaleinsatzplan_id)

        # Response und PDF-Canvas initialisieren
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{personaleinsatzplan.name}_uebersicht.pdf"'
        p = canvas.Canvas(response)

        # Titel hinzufügen
        p.drawString(100, 800, f"Personaleinsatzplan: {personaleinsatzplan.name}")
        p.drawString(100, 780, f"Startdatum: {personaleinsatzplan.startdatum}")
        p.drawString(100, 760, f"Enddatum: {personaleinsatzplan.enddatum}")
        p.drawString(100, 740, f"Kostenträger: {personaleinsatzplan.kostentraeger}")

        # Aufträge des Personaleinsatzplans hinzufügen
        y = 700
        for auftrag in personaleinsatzplan.auftraege.all():
            p.drawString(100, y, f"Auftrag: {auftrag.name}")
            y -= 20
            for schluessel in auftrag.betreuungsschluessel.all():
                p.drawString(120, y, f"Betreuungsschlüssel: {schluessel.name}")
                y -= 20
                for mitarbeiter in schluessel.mitarbeiter_zuweisungen.all():
                    p.drawString(140, y,
                                 f"Mitarbeiter: {mitarbeiter.mitarbeiter.vorname} {mitarbeiter.mitarbeiter.nachname}")
                    p.drawString(300, y, f"Anteil Stunden: {mitarbeiter.anteil_stunden_pro_woche}")
                    y -= 20

        # PDF schließen und zurückgeben
        p.showPage()
        p.save()
        return response