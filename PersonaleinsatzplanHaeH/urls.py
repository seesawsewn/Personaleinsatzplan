from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PersonaleinsatzplanCreateView, PersonaleinsatzplanDetailView,
    PersonaleinsatzplanUpdateView, PersonaleinsatzplanDeleteView,
    AuftragCreateView, AuftragListView, AuftragDetailView, AuftragUpdateView, AuftragDeleteView,
    BetreuungsschluesselCreateView,
    BetreuungsschluesselDeleteView,
    MitarbeiterCreateView, MitarbeiterListView, MitarbeiterDetailView, MitarbeiterUpdateView, MitarbeiterDeleteView,
    MitarbeiterBetreuungsschluesselCreateView,
    MitarbeiterBetreuungsschluesselDeleteView, StartseiteView, PersonaleinsatzplaeneFuerNiederlassungView,
    NiederlassungPersonaleinsatzplanuebersicht, GesamtPersonaleinsatzplanUebersicht,
    Personaleinsatzplanuebersicht,
    PersonaleinsatzplanOverviewPDFView, PersonaleinsatzplanDetail2, PersonaleinsatzplanList2View, custom_logout_view)




app_name = 'PersonaleinsatzplanHaeH'
urlpatterns = [

    path('custom-login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('', StartseiteView.as_view(), name='startseite'),
    # Personaleinsatzplan URLs
    path('personaleinsatzplan/create/', PersonaleinsatzplanCreateView.as_view(), name='personaleinsatzplan_create'),
    path("personaleinsatzplan/list/", PersonaleinsatzplanList2View.as_view(), name="personaleinsatzplan_list"),
    path('personaleinsatzplan/list2/', PersonaleinsatzplanList2View.as_view(), name='personaleinsatzplan_list2'),
    path('personaleinsatzplan/<int:pk>/', PersonaleinsatzplanDetailView.as_view(), name='personaleinsatzplan_detail'),
    path('personaleinsatzplan/<int:pk>/detail2/', PersonaleinsatzplanDetail2.as_view(), name='personaleinsatzplan_detail2'),
    path('personaleinsatzplan/<int:pk>/update/', PersonaleinsatzplanUpdateView.as_view(), name='personaleinsatzplan_update'),
    path('personaleinsatzplan/<int:pk>/delete/', PersonaleinsatzplanDeleteView.as_view(), name='personaleinsatzplan_delete'),

    # Auftrag URLs
    path('auftrag/create/', AuftragCreateView.as_view(), name='auftrag_create'),
    path('auftrag/list/', AuftragListView.as_view(), name='auftrag_list'),
    path('auftrag/<int:pk>/', AuftragDetailView.as_view(), name='auftrag_detail'),
    path('auftrag/<int:pk>/update/', AuftragUpdateView.as_view(), name='auftrag_update'),
    path('auftrag/<int:pk>/delete/', AuftragDeleteView.as_view(), name='auftrag_delete'),

    # Betreuungsschluessel URLs
    path('betreuungsschluessel/create/', BetreuungsschluesselCreateView.as_view(), name='betreuungsschluessel_create'),
    path('betreuungsschluessel/<int:pk>/delete/', BetreuungsschluesselDeleteView.as_view(), name='betreuungsschluessel_delete'),

    # Mitarbeiter URLs
    path('mitarbeiter/create/', MitarbeiterCreateView.as_view(), name='mitarbeiter_create'),
    path('mitarbeiter/list/', MitarbeiterListView.as_view(), name='mitarbeiter_list'),
    path('mitarbeiter/<int:pk>/', MitarbeiterDetailView.as_view(), name='mitarbeiter_detail'),
    path('mitarbeiter/<int:pk>/update/', MitarbeiterUpdateView.as_view(), name='mitarbeiter_update'),
    path('mitarbeiter/<int:pk>/delete/', MitarbeiterDeleteView.as_view(), name='mitarbeiter_delete'),


    # MitarbeiterBetreuungsschluessel URLs
    path('mitarbeiter-betreuungsschluessel/create/<int:schluessel_id>/', MitarbeiterBetreuungsschluesselCreateView.as_view(), name='mitarbeiter_betreuungsschluessel_create'),
    path('mitarbeiter-betreuungsschluessel/<int:pk>/delete/', MitarbeiterBetreuungsschluesselDeleteView.as_view(), name='mitarbeiter_betreuungsschluessel_delete'),



    # Personaleinsatzplan Übersicht
    path('personaleinsatzplan/<int:pk>/uebersicht/', Personaleinsatzplanuebersicht.as_view(), name='personaleinsatzplan_uebersicht'),

    path('niederlassung/<int:pk>/personaleinsatzplan_uebersicht/', NiederlassungPersonaleinsatzplanuebersicht.as_view(), name='niederlassung_personaleinsatzplan_uebersicht'),

    path('personaleinsatzplaene/gesamt-uebersicht/', GesamtPersonaleinsatzplanUebersicht.as_view(), name='gesamt_personaleinsatzplan_uebersicht'),

    # Personaleinsatzplanübersicht Ausgabe als PDF Bericht

    path('personaleinsatzplaene/pdf/', PersonaleinsatzplanOverviewPDFView.as_view(), name='alle_personaleinsatzplaene_pdf'),
    path('personaleinsatzplan/<int:pk>/pdf/', PersonaleinsatzplanOverviewPDFView.as_view(), name='personaleinsatzplan_pdf'),
    path('niederlassung/<int:niederlassung_pk>/personaleinsatzplaene/pdf/', PersonaleinsatzplanOverviewPDFView.as_view(), name='niederlassung_personaleinsatzplaene_pdf'),

    path('personaleinsatzplan/<int:pk>/pdf/', PersonaleinsatzplanOverviewPDFView.as_view(), name='personaleinsatzplan_pdf'),
    path('niederlassung/<int:niederlassung_pk>/personaleinsatzplaene/pdf/', PersonaleinsatzplanOverviewPDFView.as_view(), name='niederlassung_personaleinsatzplaene_pdf'),
    # Neue urls für Anwendungsversion

    path('niederlassung/<int:pk>/personaleinsatzplaene/', PersonaleinsatzplaeneFuerNiederlassungView.as_view(), name='personaleinsatzplaene_fuer_niederlassung'),
]

