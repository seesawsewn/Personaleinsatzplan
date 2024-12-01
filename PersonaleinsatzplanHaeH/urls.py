from django.urls import path
from .views import (
    PersonaleinsatzplanCreateView, PersonaleinsatzplanDetailView,
    PersonaleinsatzplanUpdateView, PersonaleinsatzplanDeleteView,
    AuftragCreateView, AuftragListView, AuftragDetailView, AuftragUpdateView, AuftragDeleteView,
    BetreuungsschluesselCreateView, BetreuungsschluesselListView, BetreuungsschluesselDetailView,
    BetreuungsschluesselUpdateView, BetreuungsschluesselDeleteView,
    MitarbeiterCreateView, MitarbeiterListView, MitarbeiterDetailView, MitarbeiterUpdateView, MitarbeiterDeleteView,
    NiederlassungCreateView, NiederlassungListView, NiederlassungDetailView, NiederlassungUpdateView,
    NiederlassungDeleteView,
    PositionCreateView, PositionListView, PositionDetailView, PositionUpdateView, PositionDeleteView,
    PersonaleinsatzplanStatusCreateView, PersonaleinsatzplanStatusListView, PersonaleinsatzplanStatusDetailView,
    PersonaleinsatzplanStatusUpdateView, PersonaleinsatzplanStatusDeleteView,
    VollzeitaequivalentStundenCreateView, VollzeitaequivalentStundenListView, VollzeitaequivalentStundenDetailView,
    VollzeitaequivalentStundenUpdateView, VollzeitaequivalentStundenDeleteView,
    MitarbeiterBetreuungsschluesselCreateView, MitarbeiterBetreuungsschluesselListView,
    MitarbeiterBetreuungsschluesselDetailView, MitarbeiterBetreuungsschluesselUpdateView,
    MitarbeiterBetreuungsschluesselDeleteView, StartseiteView, PersonaleinsatzplaeneFuerNiederlassungView,
    NiederlassungPersonaleinsatzplanuebersicht, GesamtPersonaleinsatzplanUebersicht,
    Personaleinsatzplanuebersicht,
    PersonaleinsatzplanOverviewPDFView, PersonaleinsatzplanDetail2, PersonaleinsatzplanList2View
)


app_name = 'PersonaleinsatzplanHaeH'
urlpatterns = [

    path('', StartseiteView.as_view(), name='startseite'),

    # Personaleinsatzplan URLs
    path('personaleinsatzplan/create/', PersonaleinsatzplanCreateView.as_view(), name='personaleinsatzplan_create'),
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
    path('betreuungsschluessel/', BetreuungsschluesselListView.as_view(), name='betreuungsschluessel_list'),
    path('betreuungsschluessel/<int:pk>/', BetreuungsschluesselDetailView.as_view(), name='betreuungsschluessel_detail'),
    path('betreuungsschluessel/<int:pk>/update/', BetreuungsschluesselUpdateView.as_view(), name='betreuungsschluessel_update'),
    path('betreuungsschluessel/<int:pk>/delete/', BetreuungsschluesselDeleteView.as_view(), name='betreuungsschluessel_delete'),

    # Mitarbeiter URLs
    path('mitarbeiter/create/', MitarbeiterCreateView.as_view(), name='mitarbeiter_create'),
    path('mitarbeiter/list/', MitarbeiterListView.as_view(), name='mitarbeiter_list'),
    path('mitarbeiter/<int:pk>/', MitarbeiterDetailView.as_view(), name='mitarbeiter_detail'),
    path('mitarbeiter/<int:pk>/update/', MitarbeiterUpdateView.as_view(), name='mitarbeiter_update'),
    path('mitarbeiter/<int:pk>/delete/', MitarbeiterDeleteView.as_view(), name='mitarbeiter_delete'),

    # Niederlassung URLs
    path('niederlassung/create/', NiederlassungCreateView.as_view(), name='niederlassung_create'),
    path('niederlassung/', NiederlassungListView.as_view(), name='niederlassung_list'),
    path('niederlassung/<int:pk>/', NiederlassungDetailView.as_view(), name='niederlassung_detail'),
    path('niederlassung/<int:pk>/update/', NiederlassungUpdateView.as_view(), name='niederlassung_update'),
    path('niederlassung/<int:pk>/delete/', NiederlassungDeleteView.as_view(), name='niederlassung_delete'),

    # Position URLs
    path('position/create/', PositionCreateView.as_view(), name='position_create'),
    path('position/', PositionListView.as_view(), name='position_list'),
    path('position/<int:pk>/', PositionDetailView.as_view(), name='position_detail'),
    path('position/<int:pk>/update/', PositionUpdateView.as_view(), name='position_update'),
    path('position/<int:pk>/delete/', PositionDeleteView.as_view(), name='position_delete'),

    # PersonaleinsatzplanStatus URLs
    path('personaleinsatzplanstatus/create/', PersonaleinsatzplanStatusCreateView.as_view(), name='personaleinsatzplanstatus_create'),
    path('personaleinsatzplanstatus/', PersonaleinsatzplanStatusListView.as_view(), name='personaleinsatzplanstatus_list'),
    path('personaleinsatzplanstatus/<int:pk>/', PersonaleinsatzplanStatusDetailView.as_view(), name='personaleinsatzplanstatus_detail'),
    path('personaleinsatzplanstatus/<int:pk>/update/', PersonaleinsatzplanStatusUpdateView.as_view(), name='personaleinsatzplanstatus_update'),
    path('personaleinsatzplanstatus/<int:pk>/delete/', PersonaleinsatzplanStatusDeleteView.as_view(), name='personaleinsatzplanstatus_delete'),

    # VollzeitaequivalentStunden URLs
    path('vollzeitaequivalentstunden/create/', VollzeitaequivalentStundenCreateView.as_view(), name='vollzeitaequivalentstunden_create'),
    path('vollzeitaequivalentstunden/', VollzeitaequivalentStundenListView.as_view(), name='vollzeitaequivalentstunden_list'),
    path('vollzeitaequivalentstunden/<int:pk>/', VollzeitaequivalentStundenDetailView.as_view(), name='vollzeitaequivalentstunden_detail'),
    path('vollzeitaequivalentstunden/<int:pk>/update/', VollzeitaequivalentStundenUpdateView.as_view(), name='vollzeitaequivalentstunden_update'),
    path('vollzeitaequivalentstunden/<int:pk>/delete/', VollzeitaequivalentStundenDeleteView.as_view(), name='vollzeitaequivalentstunden_delete'),

    # MitarbeiterBetreuungsschluessel URLs
    path('mitarbeiter-betreuungsschluessel/create/<int:schluessel_id>/', MitarbeiterBetreuungsschluesselCreateView.as_view(), name='mitarbeiter_betreuungsschluessel_create'),
    path('mitarbeiter-betreuungsschluessel/', MitarbeiterBetreuungsschluesselListView.as_view(), name='mitarbeiter_betreuungsschluessel_list'),
    path('mitarbeiter-betreuungsschluessel/<int:pk>/', MitarbeiterBetreuungsschluesselDetailView.as_view(), name='mitarbeiter_betreuungsschluessel_detail'),
    path('mitarbeiter-betreuungsschluessel/<int:pk>/update/', MitarbeiterBetreuungsschluesselUpdateView.as_view(), name='mitarbeiter_betreuungsschluessel_update'),
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

