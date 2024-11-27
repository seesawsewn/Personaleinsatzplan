from django.urls import path
from . import views

app_name = 'PersonaleinsatzplanHaeH'

urlpatterns = [
    # Startseite
    path('', views.StartseiteView.as_view(), name='startseite'),

    # Personaleinsatzplan
    path('personaleinsatzplan/', views.PersonaleinsatzplanListView.as_view(), name='personaleinsatzplan_list'),
    path('personaleinsatzplan/create/', views.PersonaleinsatzplanCreateView.as_view(), name='personaleinsatzplan_create'),
    path('personaleinsatzplan/<int:pk>/', views.PersonaleinsatzplanDetailView.as_view(), name='personaleinsatzplan_detail'),
    path('personaleinsatzplan/<int:pk>/update/', views.PersonaleinsatzplanUpdateView.as_view(), name='personaleinsatzplan_update'),
    path('personaleinsatzplan/<int:pk>/delete/', views.PersonaleinsatzplanDeleteView.as_view(), name='personaleinsatzplan_delete'),
    path('personaleinsatzplan/<int:pk>/uebersicht/', views.Personaleinsatzplanuebersicht.as_view(), name='personaleinsatzplan_uebersicht'),
    path('personaleinsatzplan/niederlassung/<int:pk>/', views.PersonaleinsatzplaeneFuerNiederlassungView.as_view(), name='personaleinsatzplan_niederlassung'),
    path('personaleinsatzplan/gesamtuebersicht/', views.GesamtPersonaleinsatzplanUebersicht.as_view(), name='gesamt_personaleinsatzplan_uebersicht'),
    path('personaleinsatzplan/pdf/<int:pk>/', views.PersonaleinsatzplanOverviewPDFView.as_view(), name='personaleinsatzplan_pdf'),
    path('niederlassung/<int:pk>/personaleinsatzplaene/pdf/', views.NiederlassungPersonaleinsatzplanuebersicht.as_view(), name='niederlassung_personaleinsatzplaene_pdf'),

    # Auftrag
    path('auftrag/', views.AuftragListView.as_view(), name='auftrag_list'),
    path('auftrag/create/', views.AuftragCreateView.as_view(), name='auftrag_create'),
    path('auftrag/<int:pk>/', views.AuftragDetailView.as_view(), name='auftrag_detail'),
    path('auftrag/<int:pk>/update/', views.AuftragUpdateView.as_view(), name='auftrag_update'),
    path('auftrag/<int:pk>/delete/', views.AuftragDeleteView.as_view(), name='auftrag_delete'),

    # Betreuungsschlüssel
    path('betreuungsschluessel/', views.BetreuungsschluesselListView.as_view(), name='betreuungsschluessel_list'),
    path('betreuungsschluessel/create/', views.BetreuungsschluesselCreateView.as_view(), name='betreuungsschluessel_create'),
    path('betreuungsschluessel/<int:pk>/', views.BetreuungsschluesselDetailView.as_view(), name='betreuungsschluessel_detail'),
    path('betreuungsschluessel/<int:pk>/update/', views.BetreuungsschluesselUpdateView.as_view(), name='betreuungsschluessel_update'),
    path('betreuungsschluessel/<int:pk>/delete/', views.BetreuungsschluesselDeleteView.as_view(), name='betreuungsschluessel_delete'),

    # Mitarbeiter
    path('mitarbeiter/', views.MitarbeiterListView.as_view(), name='mitarbeiter_list'),
    path('mitarbeiter/create/', views.MitarbeiterCreateView.as_view(), name='mitarbeiter_create'),
    path('mitarbeiter/<int:pk>/', views.MitarbeiterDetailView.as_view(), name='mitarbeiter_detail'),
    path('mitarbeiter/<int:pk>/update/', views.MitarbeiterUpdateView.as_view(), name='mitarbeiter_update'),
    path('mitarbeiter/<int:pk>/delete/', views.MitarbeiterDeleteView.as_view(), name='mitarbeiter_delete'),

    # Mitarbeiter-Betreuungsschlüssel
    path('mitarbeiter_betreuungsschluessel/', views.MitarbeiterBetreuungsschluesselListView.as_view(), name='mitarbeiter_betreuungsschluessel_list'),
    path('mitarbeiter_betreuungsschluessel/create/<int:schluessel_id>/', views.MitarbeiterBetreuungsschluesselCreateView.as_view(), name='mitarbeiter_betreuungsschluessel_create'),
    path('mitarbeiter_betreuungsschluessel/<int:pk>/', views.MitarbeiterBetreuungsschluesselDetailView.as_view(), name='mitarbeiter_betreuungsschluessel_detail'),
    path('mitarbeiter_betreuungsschluessel/<int:pk>/update/', views.MitarbeiterBetreuungsschluesselUpdateView.as_view(), name='mitarbeiter_betreuungsschluessel_update'),
    path('mitarbeiter_betreuungsschluessel/<int:pk>/delete/', views.MitarbeiterBetreuungsschluesselDeleteView.as_view(), name='mitarbeiter_betreuungsschluessel_delete'),

    # Niederlassung
    path('niederlassung/', views.NiederlassungListView.as_view(), name='niederlassung_list'),
    path('niederlassung/create/', views.NiederlassungCreateView.as_view(), name='niederlassung_create'),
    path('niederlassung/<int:pk>/', views.NiederlassungDetailView.as_view(), name='niederlassung_detail'),
    path('niederlassung/<int:pk>/update/', views.NiederlassungUpdateView.as_view(), name='niederlassung_update'),
    path('niederlassung/<int:pk>/delete/', views.NiederlassungDeleteView.as_view(), name='niederlassung_delete'),

path(
    'personaleinsatzplan/niederlassung/<int:pk>/',
    views.PersonaleinsatzplaeneFuerNiederlassungView.as_view(),
    name='personaleinsatzplaene_fuer_niederlassung',
)


]
