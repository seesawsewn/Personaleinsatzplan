from django.db.models import Sum
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse
from .models import Auftrag, Personaleinsatzplan, Betreuungsschluessel, Mitarbeiter, Niederlassung, Position, \
    PersonaleinsatzplanStatus, MitarbeiterBetreuungsschluessel, VollzeitaequivalentStunden
from django.shortcuts import redirect
from .forms import MitarbeiterZuweisungForm, MitarbeiterBetreuungsschluesselForm, MitarbeiterForm, \
    BetreuungsschluesselForm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import PersonaleinsatzplanForm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy





class StartseiteView(TemplateView):
    template_name = 'startseite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Füge alle Niederlassungen dem Kontext hinzu
        context['niederlassungen'] = Niederlassung.objects.all()
        return context


# Erstellen eines Personaleinsatzplans



class PersonaleinsatzplanCreateView(CreateView):
    model = Personaleinsatzplan
    form_class = PersonaleinsatzplanForm
    template_name = 'personaleinsatzplan_form.html'

    def get_initial(self):
        initial = super().get_initial()
        niederlassung_id = self.request.GET.get('niederlassung_id')  # Hole die Niederlassung aus der GET-Anfrage
        if niederlassung_id:
            try:
                initial['niederlassung'] = Niederlassung.objects.get(pk=niederlassung_id)
            except Niederlassung.DoesNotExist:
                pass  # Falls keine gültige Niederlassung gefunden wird, überspringe
        return initial

    def get_success_url(self):
        # Prüfe den `next`-Parameter
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        # Standard-Redirect zur Personaleinsatzplan-Liste
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_list')

    def get_context_data(self, **kwargs):
        # Standard-Kontextdaten von CreateView übernehmen
        context = super().get_context_data(**kwargs)
        # Rück-Link zur vorherigen Seite oder zur Startseite
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context




# Liste aller Personaleinsatzpläne anzeigen
class PersonaleinsatzplanList2View(ListView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_list2.html'
    context_object_name = 'personaleinsatzplaene'

    def get_queryset(self):
        # Hole alle Personaleinsatzpläne
        queryset = super().get_queryset()

        # Filter nach Niederlassung, falls im GET-Parameter vorhanden
        niederlassung_id = self.request.GET.get('niederlassung')
        if niederlassung_id:
            queryset = queryset.filter(niederlassung_id=niederlassung_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Füge alle Niederlassungen und den aktuellen Filter zum Kontext hinzu
        context['niederlassungen'] = Niederlassung.objects.all()
        context['zurueck_link'] = self.request.GET.get('next', '/')
        return context


# Detailansicht eines Personaleinsatzplans
class PersonaleinsatzplanDetailView(DetailView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_detail2.html'
    context_object_name = 'personaleinsatzplan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personaleinsatzplan = self.object

        # Lade die Aufträge und dazugehörige Betreuungsschlüssel
        auftrag_details = []
        auftraege = Auftrag.objects.filter(personaleinsatzplan=personaleinsatzplan).prefetch_related(
            'betreuungsschluessel__mitarbeiter_zuweisungen__mitarbeiter'
        )

        for auftrag in auftraege:
            betreuungsschluessel_details = []
            for schluessel in auftrag.betreuungsschluessel.all():
                mitarbeiter_zuweisungen = schluessel.mitarbeiter_zuweisungen.all()

                # Mitarbeiterdaten sammeln
                mitarbeiter_list = []
                for zuweisung in mitarbeiter_zuweisungen:
                    mitarbeiter_list.append({
                        'id': zuweisung.mitarbeiter.id,
                        'nachname': zuweisung.mitarbeiter.nachname,
                        'vorname': zuweisung.mitarbeiter.vorname,
                        'geburtsdatum': zuweisung.mitarbeiter.geburtsdatum,
                        'qualifikation': zuweisung.mitarbeiter.qualifikation,
                        'max_woechentliche_arbeitszeit': zuweisung.mitarbeiter.max_woechentliche_arbeitszeit,
                        'anteil_stunden_pro_woche': zuweisung.anteil_stunden_pro_woche,
                        'freie_stunden': zuweisung.freie_stunden,
                        'zugewiesene_stunden': zuweisung.total_hours,
                        'kommentar': zuweisung.kommentar,
                        'mitarbeiter_betreuungsschluessel_id': zuweisung.id,
                    })

                # Betreuungsschlüsseldetails sammeln
                betreuungsschluessel_details.append({
                    'id': schluessel.id,
                    'name': schluessel.name,
                    'position': schluessel.position,
                    'klienten_pro_betreuer': schluessel.klienten_pro_betreuer,
                    'benoetigte_VZA_max': schluessel.benoetigte_VZA_max,
                    'benoetigte_VZA_mindest': schluessel.benoetigte_VZA_mindest,
                    'benoetigte_VZA_aktuell': schluessel.benoetigte_VZA_aktuell,
                    'abgedeckte_VZA': schluessel.abgedeckte_VZA,
                    'differenz_VZA_max': schluessel.differenz_VZA_max,
                    'differenz_VZA_mindest': schluessel.differenz_VZA_mindest,
                    'differenz_VZA_aktuell': schluessel.differenz_VZA_aktuell,
                    'mitarbeiter': mitarbeiter_list,
                })

            # Auftragsdetails sammeln
            auftrag_details.append({
                'auftrag': auftrag,
                'betreuungsschluessel': betreuungsschluessel_details,
            })

        # Füge die Daten dem Kontext hinzu
        context['auftrag_details'] = auftrag_details

        # Rück-Link zur vorherigen Seite oder Standard auf die Startseite setzen
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context


class PersonaleinsatzplanDetail2(DetailView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_detail2.html'
    context_object_name = 'personaleinsatzplan'

    def get_context_data(self, **kwargs):
        # Standard-Kontextdaten übernehmen
        context = super().get_context_data(**kwargs)

        # `next`-Parameter auslesen, Standardwert: Startseite
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context

        # Aufträge des Personaleinsatzplans in den Kontext hinzufügen
        context['auftraege'] = self.object.auftraege.all()

        return context



# Aktualisieren eines Personaleinsatzplans
class PersonaleinsatzplanUpdateView(UpdateView):
    model = Personaleinsatzplan
    fields = ['name', 'gueltigkeit_monat', 'gueltigkeit_jahr', 'kostentraeger', 'ersteller', 'version', 'status', 'niederlassung']
    template_name = 'personaleinsatzplan_form.html'

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_list')


# Löschen eines Personaleinsatzplans

class PersonaleinsatzplanDeleteView(DeleteView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_confirm_delete.html'
    success_url = reverse_lazy('startseite')

    def post(self, request, *args, **kwargs):
        """
        Überschreibe die POST-Methode, um den ProtectedError korrekt abzufangen.
        """
        self.object = self.get_object()
        try:
            # Versuche, das Objekt zu löschen
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except ProtectedError as e:
            # ProtectedError abfangen und Kontextdaten vorbereiten
            related_objects = [str(obj) for obj in e.protected_objects]
            context = self.get_context_data()
            context['error_message'] = (
                "Der Personaleinsatzplan kann nicht gelöscht werden, die folgenden Mitarbeiter:innen sind noch zugewiesen."
            )
            context['related_objects'] = related_objects
            return self.render_to_response(context)





# Erstellen eines Auftrags
class AuftragCreateView(CreateView):
    model = Auftrag
    fields = [
        'name', 'vergabenummer', 'optionsnummer', 'massnahmenummer', 'startdatum', 'enddatum',
        'max_klienten', 'mindest_klienten', 'aktuell_klienten', 'personaleinsatzplan'
    ]
    template_name = 'auftrag_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # Übernehme den Personaleinsatzplan aus der URL, falls übergeben
        personaleinsatzplan_id = self.request.GET.get('personaleinsatzplan_id')
        if personaleinsatzplan_id:
            initial['personaleinsatzplan'] = personaleinsatzplan_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Füge den Personaleinsatzplan in den Kontext hinzu (optional)
        personaleinsatzplan_id = self.request.GET.get('personaleinsatzplan_id')
        if personaleinsatzplan_id:
            context['personaleinsatzplan'] = personaleinsatzplan_id
        return context

    def get_success_url(self):
        # Weiterleitung zur vorherigen Seite oder Standard-Redirect
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('PersonaleinsatzplanHaeH:auftrag_list')


# Liste aller Aufträge anzeigen


class AuftragListView(ListView):
    model = Auftrag
    template_name = 'auftrag_list.html'
    context_object_name = 'auftraege'

    def get_queryset(self):
        # Hole alle Aufträge
        queryset = super().get_queryset()

        # Filter nach Niederlassung, falls im GET-Parameter vorhanden
        niederlassung_id = self.request.GET.get('niederlassung')
        if niederlassung_id:
            queryset = queryset.filter(personaleinsatzplan__niederlassung_id=niederlassung_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Füge alle Niederlassungen und den aktuellen Filter zum Kontext hinzu
        context['niederlassungen'] = Niederlassung.objects.all()
        context['zurueck_link'] = self.request.GET.get('next', '/')
        return context


# Detailansicht eines Auftrags


class AuftragDetailView(DetailView):
    model = Auftrag
    template_name = 'auftrag_detail.html'
    context_object_name = 'auftrag'

    def get_context_data(self, **kwargs):
        # Standard-Kontextdaten übernehmen
        context = super().get_context_data(**kwargs)
        betreuungsschluessel_details = []

        # Sammeln der Betreuungsschlüssel und zugewiesenen Mitarbeiter
        for schluessel in self.object.betreuungsschluessel.all():
            mitarbeiter_details = []
            for zuweisung in schluessel.mitarbeiter_zuweisungen.all():
                mitarbeiter_details.append({
                    'mitarbeiter': zuweisung.mitarbeiter,
                    'geburtsdatum': zuweisung.mitarbeiter.geburtsdatum,
                    'qualifikation': zuweisung.mitarbeiter.qualifikation,
                    'max_woechentliche_arbeitszeit': zuweisung.mitarbeiter.max_woechentliche_arbeitszeit,
                    'anteil_stunden_pro_woche': zuweisung.anteil_stunden_pro_woche,
                    'freie_stunden': zuweisung.freie_stunden,
                    'zugewiesene_stunden': zuweisung.total_hours,
                    'kommentar': zuweisung.kommentar,
                })
            betreuungsschluessel_details.append({
                'schluessel': schluessel,
                'mitarbeiter_details': mitarbeiter_details,
            })

        # Kontext hinzufügen
        context['betreuungsschluessel_details'] = betreuungsschluessel_details
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context


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

    def get_success_url(self):
        # Standard-Redirect zur Auftragsliste
        return reverse_lazy('PersonaleinsatzplanHaeH:personaleinsatzplan_list2')

    def post(self, request, *args, **kwargs):
        """
        Überschreibe die POST-Methode, um den ProtectedError korrekt abzufangen.
        """
        self.object = self.get_object()
        next_url = request.POST.get('next')  # Nimm den 'next'-Parameter aus dem POST-Request
        try:
            # Versuche, das Objekt zu löschen
            self.object.delete()
            # Weiterleitung basierend auf 'next' oder Standard-URL
            return HttpResponseRedirect(next_url or self.get_success_url())
        except ProtectedError as e:
            # ProtectedError abfangen und Kontextdaten vorbereiten
            related_objects = [str(obj) for obj in e.protected_objects]
            context = self.get_context_data()
            context['error_message'] = (
                "Der Auftrag kann nicht gelöscht werden, da folgende Objekte noch mit diesem Auftrag verknüpft sind."
            )
            context['related_objects'] = related_objects
            return self.render_to_response(context)


# Erstellen eines Betreuungsschlüssels

class BetreuungsschluesselCreateView(CreateView):
    model = Betreuungsschluessel
    form_class = BetreuungsschluesselForm
    template_name = 'betreuungsschluessel_form.html'

    def get_success_url(self):
        # Hole die 'next'-URL aus den GET- oder POST-Daten
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url  # Zurück zur vorherigen Seite
        # Standard-Redirect, falls keine 'next'-URL vorhanden ist
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_list')

    def get_initial(self):
        initial = super().get_initial()
        auftrag_id = self.request.GET.get('auftrag_id')
        if auftrag_id:
            auftrag = Auftrag.objects.get(pk=auftrag_id)
            initial['auftrag'] = auftrag
        return initial

    def form_valid(self, form):
        # Name automatisch generieren
        position = form.cleaned_data['position']
        form.instance.name = f"{position.bezeichnung}"
        return super().form_valid(form)



# Liste aller Betreuungsschlüssel anzeigen
class BetreuungsschluesselListView(ListView):
    model = Betreuungsschluessel
    template_name = 'betreuungsschluessel_list.html'
    context_object_name = 'betreuungsschluessel'

    def get_context_data(self, **kwargs):
        # Standard-Kontextdaten übernehmen
        context = super().get_context_data(**kwargs)
        # Rück-Link zur vorherigen Seite oder Standard auf die Startseite setzen
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context

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

    def get_success_url(self):
        # Weiterleitung zu den Auftragsdetails
        auftrag = self.object.auftrag
        return reverse('PersonaleinsatzplanHaeH:auftrag_detail', kwargs={'pk': auftrag.pk})

    def post(self, request, *args, **kwargs):
        """
        Überschreibe die POST-Methode, um den ProtectedError korrekt abzufangen.
        """
        self.object = self.get_object()
        try:
            # Versuche, das Objekt zu löschen
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError as e:
            # ProtectedError abfangen und Kontextdaten vorbereiten
            related_objects = [str(obj) for obj in e.protected_objects]
            context = self.get_context_data()
            context['error_message'] = (
                "Der Betreuungsschlüssel kann nicht gelöscht werden, da noch Mitarbeiter:innen oder andere Objekte zugewiesen sind."
            )
            context['related_objects'] = related_objects
            return self.render_to_response(context)



# Erstellen eines Mitarbeiters
class MitarbeiterCreateView(CreateView):
    model = Mitarbeiter
    form_class = MitarbeiterForm
    template_name = 'mitarbeiter_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # Übergebe niederlassung_id aus der URL, falls vorhanden
        niederlassung_id = self.request.GET.get('niederlassung_id')  # oder self.kwargs.get('niederlassung_id')
        if niederlassung_id:
            try:
                initial['niederlassung'] = Niederlassung.objects.get(pk=niederlassung_id)
            except Niederlassung.DoesNotExist:
                pass  # Keine gültige Niederlassung gefunden
        return initial

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('PersonaleinsatzplanHaeH:mitarbeiter_list')


# Liste aller Mitarbeiter anzeigen

class MitarbeiterListView(ListView):
    model = Mitarbeiter
    template_name = 'mitarbeiter_list.html'
    context_object_name = 'mitarbeiter'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filterung nach Niederlassung
        niederlassung_id = self.request.GET.get('niederlassung')
        if niederlassung_id:
            queryset = queryset.filter(niederlassung_id=niederlassung_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Alle Niederlassungen für den Filter
        context['niederlassungen'] = Niederlassung.objects.all()

        # Name der ausgewählten Niederlassung oder Standardwert
        niederlassung_id = self.request.GET.get('niederlassung')
        if niederlassung_id:
            niederlassung = Niederlassung.objects.filter(id=niederlassung_id).first()
            context['niederlassung_name'] = niederlassung.name if niederlassung else "Alle Standorte"
        else:
            context['niederlassung_name'] = "Alle Standorte"

        context['zurueck_link'] = self.request.GET.get('next', '/')
        return context




# Detailansicht eines Mitarbeiters
class MitarbeiterDetailView(DetailView):
    model = Mitarbeiter
    template_name = 'mitarbeiter_detail.html'
    context_object_name = 'mitarbeiter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mitarbeiter = self.object

        betreuungsschluessel_zuweisungen = MitarbeiterBetreuungsschluessel.objects.filter(mitarbeiter=mitarbeiter)

        total_hours = betreuungsschluessel_zuweisungen.aggregate(Sum('zugewiesene_stunden'))[
                          'zugewiesene_stunden__sum'] or 0
        free_hours = mitarbeiter.max_woechentliche_arbeitszeit - total_hours

        context['total_hours'] = total_hours
        context['free_hours'] = free_hours

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

        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))

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

    def get_success_url(self):
        # Weiterleitung zur Liste aller Mitarbeiter nach erfolgreichem Löschen
        return reverse_lazy('PersonaleinsatzplanHaeH:mitarbeiter_list')

    def post(self, request, *args, **kwargs):
        """
        Überschreibe die POST-Methode, um den ProtectedError korrekt abzufangen.
        """
        self.object = self.get_object()
        try:
            # Versuche, den Mitarbeiter zu löschen
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError as e:
            # ProtectedError abfangen und den zugehörigen Auftrag ermitteln
            related_objects = e.protected_objects

            # Extrahiere alle zugehörigen Aufträge
            auftraege = set()
            for obj in related_objects:
                if isinstance(obj, MitarbeiterBetreuungsschluessel):
                    betreuungsschluessel = obj.schluessel
                    if betreuungsschluessel and betreuungsschluessel.auftrag:
                        auftraege.add(betreuungsschluessel.auftrag)

            context = self.get_context_data()
            context['error_message'] = (
                "Der Mitarbeiter kann nicht gelöscht werden, da er einem oder mehreren Aufträgen "
                "zugeordnet ist."
            )
            context['related_auftraege'] = list(auftraege)
            return self.render_to_response(context)






class MitarbeiterBetreuungsschluesselCreateView(CreateView):
    model = MitarbeiterBetreuungsschluessel
    form_class = MitarbeiterBetreuungsschluesselForm
    template_name = 'mitarbeiter_betreuungsschluessel_form.html'

    def get_initial(self):
        initial = super().get_initial()
        schluessel_id = self.kwargs.get('schluessel_id')
        if schluessel_id:
            schluessel = Betreuungsschluessel.objects.get(pk=schluessel_id)
            initial['schluessel'] = schluessel
            initial['position'] = schluessel.position
            initial['auftrag'] = schluessel.auftrag
        return initial

    def form_valid(self, form):
        schluessel_id = self.kwargs.get('schluessel_id')
        if schluessel_id:
            schluessel = Betreuungsschluessel.objects.get(pk=schluessel_id)
            form.instance.schluessel = schluessel
            form.instance.position = schluessel.position
            form.instance.auftrag = schluessel.auftrag
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_detail', kwargs={'pk': self.object.schluessel.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schluessel_id = self.kwargs.get('schluessel_id')
        if schluessel_id:
            schluessel = Betreuungsschluessel.objects.get(pk=schluessel_id)
            personaleinsatzplan = schluessel.auftrag.personaleinsatzplan

            # Filtere die Betreuungsschlüssel für den gleichen Zeitraum wie der zugehörige Personaleinsatzplan
            relevante_personaleinsatzplaene = Personaleinsatzplan.objects.filter(
                gueltigkeit_monat=personaleinsatzplan.gueltigkeit_monat,
                gueltigkeit_jahr=personaleinsatzplan.gueltigkeit_jahr
            )
            context['verfuegbare_betreuungsschluessel'] = Betreuungsschluessel.objects.filter(
                auftrag__personaleinsatzplan__in=relevante_personaleinsatzplaene
            )
        context['next'] = self.request.GET.get('next', '')
        return context







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
    form_class = MitarbeiterBetreuungsschluesselForm
    template_name = 'mitarbeiter_betreuungsschluessel_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zuweisung = self.object
        schluessel = zuweisung.schluessel

        # Filtere die Betreuungsschlüssel für den gleichen Zeitraum wie der zugehörige Personaleinsatzplan
        if schluessel and schluessel.auftrag and schluessel.auftrag.personaleinsatzplan:
            personaleinsatzplan = schluessel.auftrag.personaleinsatzplan
            relevante_personaleinsatzplaene = Personaleinsatzplan.objects.filter(
                gueltigkeit_monat=personaleinsatzplan.gueltigkeit_monat,
                gueltigkeit_jahr=personaleinsatzplan.gueltigkeit_jahr
            )
            context['verfuegbare_betreuungsschluessel'] = Betreuungsschluessel.objects.filter(
                auftrag__personaleinsatzplan__in=relevante_personaleinsatzplaene
            )
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('PersonaleinsatzplanHaeH:betreuungsschluessel_detail', kwargs={'pk': self.object.schluessel.pk})


# Löschen eines MitarbeiterBetreuungsschluessel

class MitarbeiterBetreuungsschluesselDeleteView(DeleteView):
    model = MitarbeiterBetreuungsschluessel
    template_name = 'mitarbeiter_betreuungsschluessel_confirm_delete.html'

    def get_success_url(self):
        # Hole den zugehörigen Betreuungsschlüssel
        betreuungsschluessel = self.object.schluessel

        # Hole den zugehörigen Personaleinsatzplan
        personaleinsatzplan = betreuungsschluessel.auftrag.personaleinsatzplan

        # Zurück zur Übersicht des Personaleinsatzplans
        return reverse('PersonaleinsatzplanHaeH:personaleinsatzplan_uebersicht', kwargs={'pk': personaleinsatzplan.pk})



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



class Personaleinsatzplanuebersicht(DetailView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_uebersicht.html'
    context_object_name = 'personaleinsatzplan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personaleinsatzplan = self.object

        # Aufträge des Personaleinsatzplans abrufen
        auftraege = Auftrag.objects.filter(personaleinsatzplan=personaleinsatzplan).prefetch_related(
            'betreuungsschluessel__mitarbeiter_zuweisungen__mitarbeiter'
        )

        auftrag_details = []

        # Iteriere durch die Aufträge
        for auftrag in auftraege:
            if not auftrag.id:
                continue  # Überspringe ungültige Aufträge

            betreuungsschluessel_details = []
            # Betreuungsschlüssel des Auftrags abrufen
            betreuungsschluessel = auftrag.betreuungsschluessel.all()

            for schluessel in betreuungsschluessel:
                if not schluessel.id:
                    continue  # Überspringe ungültige Betreuungsschlüssel

                # Mitarbeiter-Zuweisungen des Betreuungsschlüssels abrufen
                mitarbeiter_zuweisungen = schluessel.mitarbeiter_zuweisungen.all()
                mitarbeiter_list = []

                for zuweisung in mitarbeiter_zuweisungen:
                    if zuweisung.mitarbeiter and zuweisung.mitarbeiter.id:
                        # Berechnung der total_hours und free_hours für jeden Mitarbeiter
                        berechnung = MitarbeiterBetreuungsschluessel.calculate_hours_and_free_time(
                            mitarbeiter=zuweisung.mitarbeiter,
                            personaleinsatzplan=personaleinsatzplan
                        )
                        mitarbeiter_list.append({
                            'id': zuweisung.mitarbeiter.id,
                            'nachname': zuweisung.mitarbeiter.nachname,
                            'vorname': zuweisung.mitarbeiter.vorname,
                            'geburtsdatum': zuweisung.mitarbeiter.geburtsdatum,
                            'qualifikation': zuweisung.mitarbeiter.qualifikation,
                            'max_woechentliche_arbeitszeit': zuweisung.mitarbeiter.max_woechentliche_arbeitszeit,
                            'anteil_stunden_pro_woche': zuweisung.anteil_stunden_pro_woche,
                            'freie_stunden': berechnung['free_hours'],  # Berechnete freie Stunden
                            'zugewiesene_stunden': berechnung['total_hours'],  # Berechnete Gesamtstunden
                            'kommentar': zuweisung.kommentar,
                            'mitarbeiter_betreuungsschluessel_id': zuweisung.id,
                        })

                # Betreuungsschlüssel-Daten hinzufügen
                betreuungsschluessel_details.append({
                    'id': schluessel.id,
                    'name': schluessel.name,
                    'position': schluessel.position,
                    'klienten_pro_betreuer': schluessel.klienten_pro_betreuer,
                    'mitarbeiter': mitarbeiter_list,
                    'benoetigte_VZA_max': schluessel.benoetigte_VZA_max,
                    'benoetigte_VZA_mindest': schluessel.benoetigte_VZA_mindest,
                    'benoetigte_VZA_aktuell': schluessel.benoetigte_VZA_aktuell,
                    'abgedeckte_VZA': schluessel.abgedeckte_VZA,
                    'differenz_VZA_max': schluessel.differenz_VZA_max,
                    'differenz_VZA_mindest': schluessel.differenz_VZA_mindest,
                    'differenz_VZA_aktuell': schluessel.differenz_VZA_aktuell,
                })

            # Auftragsdetails hinzufügen
            auftrag_details.append({
                'auftrag': auftrag,
                'betreuungsschluessel': betreuungsschluessel_details,
            })

        # Füge die Auftragsdetails zum Kontext hinzu
        context['auftrag_details'] = auftrag_details

        # Rück-Link zur vorherigen Seite oder zur Startseite hinzufügen
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))

        return context






class NiederlassungPersonaleinsatzplanuebersicht(DetailView):
    model = Niederlassung
    template_name = 'niederlassung_personaleinsatzplan_uebersicht.html'
    context_object_name = 'niederlassung'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        niederlassung = self.object

        # Alle Personaleinsatzpläne der Niederlassung abrufen
        personaleinsatzplaene = Personaleinsatzplan.objects.filter(niederlassung=niederlassung).prefetch_related(
            'auftraege__betreuungsschluessel__mitarbeiter_zuweisungen__mitarbeiter'
        )

        plandetails = []

        for plan in personaleinsatzplaene:
            auftraege = plan.auftraege.all()
            auftrag_details = []

            for auftrag in auftraege:
                betreuungsschluessel_list = auftrag.betreuungsschluessel.all()
                betreuungsschluessel_details = []

                for schluessel in betreuungsschluessel_list:
                    mitarbeiter_zuweisungen = schluessel.mitarbeiter_zuweisungen.all()
                    mitarbeiter_list = []

                    for zuweisung in mitarbeiter_zuweisungen:
                        if zuweisung.mitarbeiter:
                            mitarbeiter_list.append({
                                'id': zuweisung.mitarbeiter.id,
                                'nachname': zuweisung.mitarbeiter.nachname,
                                'vorname': zuweisung.mitarbeiter.vorname,
                                'geburtsdatum': zuweisung.mitarbeiter.geburtsdatum,
                                'qualifikation': zuweisung.mitarbeiter.qualifikation,
                                'max_woechentliche_arbeitszeit': zuweisung.mitarbeiter.max_woechentliche_arbeitszeit,
                                'anteil_stunden_pro_woche': zuweisung.anteil_stunden_pro_woche,
                                'freie_stunden': zuweisung.freie_stunden,
                                'zugewiesene_stunden': zuweisung.total_hours,  # Neues Feld hinzufügen
                                'kommentar': zuweisung.kommentar,
                                'mitarbeiter_betreuungsschluessel_id': zuweisung.id,
                            })

                    betreuungsschluessel_details.append({
                        'id': schluessel.id,
                        'name': schluessel.name,
                        'position': schluessel.position,
                        'klienten_pro_betreuer': schluessel.klienten_pro_betreuer,
                        'mitarbeiter': mitarbeiter_list,
                        'benoetigte_VZA_max': schluessel.benoetigte_VZA_max,
                        'benoetigte_VZA_mindest': schluessel.benoetigte_VZA_mindest,
                        'benoetigte_VZA_aktuell': schluessel.benoetigte_VZA_aktuell,
                        'abgedeckte_VZA': schluessel.abgedeckte_VZA,
                        'differenz_VZA_max': schluessel.differenz_VZA_max,
                        'differenz_VZA_mindest': schluessel.differenz_VZA_mindest,
                        'differenz_VZA_aktuell': schluessel.differenz_VZA_aktuell,
                    })

                auftrag_details.append({
                    'auftrag': auftrag,
                    'betreuungsschluessel': betreuungsschluessel_details,
                })

            plandetails.append({
                'plan': plan,
                'auftraege': auftrag_details,
            })

        context['plandetails'] = plandetails

        # Rück-Link zur vorherigen Seite oder zur Startseite hinzufügen
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))

        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))

        return context


class GesamtPersonaleinsatzplanUebersicht(ListView):
    model = Personaleinsatzplan
    template_name = 'gesamt_personaleinsatzplan_uebersicht.html'
    context_object_name = 'personaleinsatzplaene'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Alle Niederlassungen abrufen und die zugehörigen Personaleinsatzpläne vorladen
        niederlassungen = Niederlassung.objects.prefetch_related(
            'personaleinsatzplaene__auftraege__betreuungsschluessel__mitarbeiter_zuweisungen__mitarbeiter'
        )

        # Struktur für die niederlassung_details vorbereiten
        niederlassung_details = []

        for niederlassung in niederlassungen:
            # Abrufen der Personaleinsatzpläne pro Niederlassung
            personaleinsatzplaene = niederlassung.personaleinsatzplaene.all()

            # Nur Niederlassungen einfügen, die mindestens einen Personaleinsatzplan haben
            if personaleinsatzplaene.exists():
                plandetails = []

                for plan in personaleinsatzplaene:
                    auftraege = plan.auftraege.all()
                    auftrag_details = []

                    for auftrag in auftraege:
                        betreuungsschluessel_list = auftrag.betreuungsschluessel.all()
                        betreuungsschluessel_details = []

                        for schluessel in betreuungsschluessel_list:
                            mitarbeiter_zuweisungen = schluessel.mitarbeiter_zuweisungen.all()
                            mitarbeiter_list = [
                                {
                                    'id': m.mitarbeiter.id,
                                    'vorname': m.mitarbeiter.vorname,
                                    'nachname': m.mitarbeiter.nachname,
                                    'geburtsdatum': m.mitarbeiter.geburtsdatum,
                                    'qualifikation': m.mitarbeiter.qualifikation,
                                    'max_woechentliche_arbeitszeit': m.mitarbeiter.max_woechentliche_arbeitszeit,
                                    'anteil_stunden': m.anteil_stunden_pro_woche,
                                    'kommentar': m.kommentar,
                                }
                                for m in mitarbeiter_zuweisungen if m.mitarbeiter
                            ]

                            betreuungsschluessel_details.append({
                                'name': schluessel.name,
                                'position': schluessel.position,
                                'klienten_pro_betreuer': schluessel.klienten_pro_betreuer,
                                'mitarbeiter': mitarbeiter_list,
                                'benoetigte_VZA_max': schluessel.benoetigte_VZA_max,
                                'benoetigte_VZA_mindest': schluessel.benoetigte_VZA_mindest,
                                'benoetigte_VZA_aktuell': schluessel.benoetigte_VZA_aktuell,
                                'abgedeckte_VZA': schluessel.abgedeckte_VZA,
                                'differenz_VZA_max': schluessel.differenz_VZA_max,
                                'differenz_VZA_mindest': schluessel.differenz_VZA_mindest,
                                'differenz_VZA_aktuell': schluessel.differenz_VZA_aktuell,
                            })

                        auftrag_details.append({
                            'auftrag': auftrag,
                            'betreuungsschluessel': betreuungsschluessel_details,
                        })

                    plandetails.append({
                        'plan': plan,
                        'auftraege': auftrag_details,
                    })

                niederlassung_details.append({
                    'niederlassung': niederlassung,
                    'plandetails': plandetails,
                })

        context['niederlassung_details'] = niederlassung_details
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))

        return context



# Ausgabe einer Personaleinsatzplanübersicht als PDF Bericht


class PersonaleinsatzplanOverviewPDFView(View):
    def get(self, request, pk=None, niederlassung_pk=None, *args, **kwargs):
        # HTTP-Antwort vorbereiten, die als PDF zurückgegeben wird
        if pk:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="personaleinsatzplan_{pk}.pdf"'
        elif niederlassung_pk:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="niederlassung_{niederlassung_pk}_uebersicht.pdf"'
        else:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="alle_personaleinsatzplaene.pdf"'

        # PDF-Dokument erstellen
        doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []

        if pk:
            # Einzelnen Personaleinsatzplan abrufen
            personaleinsatzplan = get_object_or_404(Personaleinsatzplan, pk=pk)
            # Titel hinzufügen
            elements.append(self.create_title(f"Personaleinsatzplan: {personaleinsatzplan.name}"))
            elements.append(Table([[' ']]))  # Leerraum

            # Allgemeine Informationen als Tabelle hinzufügen
            elements.append(self.create_personaleinsatzplan_table(personaleinsatzplan))

            # Aufträge hinzufügen
            self.add_auftraege(personaleinsatzplan.auftraege.all(), elements)

        elif niederlassung_pk:
            # Alle Personaleinsatzpläne einer Niederlassung abrufen
            niederlassung = get_object_or_404(Niederlassung, pk=niederlassung_pk)
            personaleinsatzplaene = Personaleinsatzplan.objects.filter(niederlassung=niederlassung)
            # Titel hinzufügen
            elements.append(self.create_title(f"Personaleinsatzpläne der Niederlassung: {niederlassung.name}"))
            elements.append(Table([[' ']]))  # Leerraum

            # Schleife durch alle Personaleinsatzpläne der Niederlassung
            for plan in personaleinsatzplaene:
                elements.append(self.create_personaleinsatzplan_table(plan))
                elements.append(Table([[' ']]))  # Leerraum
                # Aufträge hinzufügen
                self.add_auftraege(plan.auftraege.all(), elements)

        else:
            # Alle Personaleinsatzpläne abrufen, geordnet nach Niederlassung
            personaleinsatzplaene = Personaleinsatzplan.objects.select_related('niederlassung').order_by('niederlassung__name')
            current_niederlassung = None

            # Schleife durch alle Personaleinsatzpläne
            for plan in personaleinsatzplaene:
                if current_niederlassung != plan.niederlassung:
                    # Wenn es eine neue Niederlassung ist, füge den Namen der Niederlassung hinzu
                    current_niederlassung = plan.niederlassung
                    elements.append(self.create_title(f"Niederlassung: {current_niederlassung.name}"))
                    elements.append(Table([[' ']]))  # Leerraum

                # Informationen zu diesem Personaleinsatzplan hinzufügen
                elements.append(self.create_personaleinsatzplan_table(plan))
                elements.append(Table([[' ']]))  # Leerraum
                # Aufträge hinzufügen
                self.add_auftraege(plan.auftraege.all(), elements)

        # PDF-Datei generieren
        doc.build(elements)
        return response

    def create_title(self, text):
        title_table = Table([[text]], colWidths=[500])  # Tabelle mit einem Titel erstellen
        title_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 20),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        return title_table

    def create_personaleinsatzplan_table(self, plan):
        data = [
            ['Personaleinsatzplan', plan.name],
            ['Gültigkeit', f"{plan.get_gueltigkeit_monat_display()} {plan.gueltigkeit_jahr}"],
            ['Kostenträger', plan.kostentraeger],
            ['Ersteller', plan.ersteller],
            ['Version', plan.version],
            ['Status', plan.status]
        ]

        table = Table(data, colWidths=[150, 350])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table

    def add_auftraege(self, auftraege, elements):
        # Stil für Zellen mit Zeilenumbruch
        cell_style = ParagraphStyle(name='CellStyle', fontName='Helvetica', fontSize=10, leading=12)

        for auftrag in auftraege:
            # Datenstruktur erstellen und Text umwandeln
            data_auftrag = [
                ['Auftrag', Paragraph(auftrag.name, cell_style), 'Vergabenummer', auftrag.vergabenummer],
                ['Optionsnummer', auftrag.optionsnummer, 'Maßnahmenummer', auftrag.massnahmenummer],
                ['Startdatum', auftrag.startdatum, 'Enddatum', auftrag.enddatum],
                ['Maximale Klienten', auftrag.max_klienten, 'Mindest Klienten', auftrag.mindest_klienten],
                ['Aktuelle Klienten', auftrag.aktuell_klienten, '', '']
            ]

            # Tabelle mit festen Spaltenbreiten erstellen
            auftrag_table = Table(data_auftrag, colWidths=[125, 125, 125, 125])

            # Tabellenstil festlegen
            auftrag_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Kopfzeile
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Links ausgerichtet
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Schriftart
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Standard-Schriftgröße
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Rahmen
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Abstand
            ]))

            # Tabelle den Elementen hinzufügen
            elements.append(auftrag_table)
            elements.append(Table([[' ']]))  # Leerraum

            # Betreuungsschlüssel hinzufügen
            cell_style = ParagraphStyle(name='CellStyle', fontName='Helvetica', fontSize=10, leading=12)

            for schluessel in auftrag.betreuungsschluessel.all():
                data_schluessel = [
                    ['Betreuungsschlüssel', Paragraph(str(schluessel.position), cell_style), 'Klienten pro Betreuer',
                     schluessel.klienten_pro_betreuer],
                    ['Benötigte VZA Max', schluessel.benoetigte_VZA_max, 'Benötigte VZA Mindest',
                     schluessel.benoetigte_VZA_mindest],
                    ['Benötigte VZA Aktuell', schluessel.benoetigte_VZA_aktuell, 'Abgedeckte VZA',
                     schluessel.abgedeckte_VZA],
                    ['VZA Differenz Max', schluessel.differenz_VZA_max, 'VZA Differenz Mindest',
                     schluessel.differenz_VZA_mindest],
                ]

                # Tabelle mit festen Spaltenbreiten erstellen
                schluessel_table = Table(data_schluessel, colWidths=[125, 125, 125, 125])

                # Tabellenstil festlegen
                schluessel_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Kopfzeile
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Links ausgerichtet
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Schriftart
                    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Standard-Schriftgröße
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Rahmen
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Abstand
                ]))

                # Tabelle den Elementen hinzufügen
                elements.append(schluessel_table)
                elements.append(Table([[' ']]))  # Leerraum

                # Mitarbeiter hinzufügen
                data_mitarbeiter = [
                    ['Mitarbeiter:in', 'Anteil Stunden', ]]
                for mitarbeiter in schluessel.mitarbeiter_zuweisungen.all():
                    # Berechnung der freien und zugewiesenen Stunden
                    berechnung = MitarbeiterBetreuungsschluessel.calculate_hours_and_free_time(
                        mitarbeiter=mitarbeiter.mitarbeiter,
                        personaleinsatzplan=schluessel.auftrag.personaleinsatzplan
                    )
                    data_mitarbeiter.append([
                        "{} {}".format(mitarbeiter.mitarbeiter.vorname, mitarbeiter.mitarbeiter.nachname),
                        mitarbeiter.anteil_stunden_pro_woche,
                    ])

                mitarbeiter_table = Table(data_mitarbeiter, colWidths=[250, 250])
                mitarbeiter_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(mitarbeiter_table)
                elements.append(Table([[' ']]))  # Leerraum zwischen Tabellen


# Neue Views für Anwendungsversion

class PersonaleinsatzplaeneFuerNiederlassungView(ListView):
    model = Personaleinsatzplan
    template_name = 'personaleinsatzplan_list.html'
    context_object_name = 'personaleinsatzplaene'

    def get_queryset(self):
        niederlassung_id = self.kwargs.get('pk')
        return Personaleinsatzplan.objects.filter(niederlassung_id=niederlassung_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['niederlassung'] = Niederlassung.objects.get(pk=self.kwargs.get('pk'))

        # `next`-Parameter auslesen, Standardwert: Startseite
        context['zurueck_link'] = self.request.GET.get('next', reverse('PersonaleinsatzplanHaeH:startseite'))
        return context

