from django.contrib import admin

# Register your models here.
from .models import (
    Niederlassung,
    Position,
    Mitarbeiter,
    PersonaleinsatzplanStatus,
    Personaleinsatzplan,
    Auftrag,
    Betreuungsschluessel,
    MitarbeiterBetreuungsschluessel,
    VollzeitaequivalentStunden
)

admin.site.register(Niederlassung)
admin.site.register(Position)
admin.site.register(Mitarbeiter)
admin.site.register(PersonaleinsatzplanStatus)
admin.site.register(Personaleinsatzplan)
admin.site.register(Auftrag)
admin.site.register(Betreuungsschluessel)
admin.site.register(MitarbeiterBetreuungsschluessel)
admin.site.register(VollzeitaequivalentStunden)