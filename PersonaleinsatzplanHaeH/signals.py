from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MitarbeiterBetreuungsschluessel

# Signal-Blockierungsvariable
signal_blocked = False

@receiver(post_save, sender=MitarbeiterBetreuungsschluessel)
def recalculate_and_store_hours_on_save(sender, instance, **kwargs):
    """
    Aktualisiert die `total_hours` und `freie_stunden`, wenn ein Mitarbeiter einem Betreuungsschlüssel
    zugewiesen oder die Zuweisung aktualisiert wird.
    """
    global signal_blocked
    if signal_blocked:
        return  # Signal blockieren, um Rekursion zu vermeiden

    if instance.mitarbeiter and instance.schluessel:
        personaleinsatzplan = instance.schluessel.auftrag.personaleinsatzplan
        if personaleinsatzplan:
            # Signal blockieren
            signal_blocked = True
            try:
                # Stunden neu berechnen
                stunden_info = MitarbeiterBetreuungsschluessel.calculate_hours_and_free_time(
                    mitarbeiter=instance.mitarbeiter,
                    personaleinsatzplan=personaleinsatzplan
                )

                # Ergebnisse nur speichern, wenn Änderungen vorliegen
                if (
                    instance.total_hours != stunden_info["total_hours"] or
                    instance.freie_stunden != stunden_info["free_hours"]
                ):
                    instance.total_hours = stunden_info["total_hours"]
                    instance.freie_stunden = stunden_info["free_hours"]
                    instance.save(update_fields=["total_hours", "freie_stunden"])
            finally:
                # Signal-Blockierung aufheben
                signal_blocked = False


@receiver(post_delete, sender=MitarbeiterBetreuungsschluessel)
def recalculate_and_store_hours_on_delete(sender, instance, **kwargs):
    """
    Aktualisiert die `total_hours` und `freie_stunden`, wenn ein Mitarbeiter aus einem Betreuungsschlüssel entfernt wird.
    """
    if instance.mitarbeiter and instance.schluessel:
        personaleinsatzplan = instance.schluessel.auftrag.personaleinsatzplan
        if personaleinsatzplan:
            # Stunden neu berechnen
            stunden_info = MitarbeiterBetreuungsschluessel.calculate_hours_and_free_time(
                mitarbeiter=instance.mitarbeiter,
                personaleinsatzplan=personaleinsatzplan
            )

            # Verbleibende Einträge aktualisieren
            MitarbeiterBetreuungsschluessel.objects.filter(
                mitarbeiter=instance.mitarbeiter,
                schluessel__auftrag__personaleinsatzplan=personaleinsatzplan
            ).update(
                total_hours=stunden_info["total_hours"],
                freie_stunden=stunden_info["free_hours"]
            )
