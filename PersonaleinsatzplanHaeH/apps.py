from django.apps import AppConfig


class PersonaleinsatzplanhaehConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PersonaleinsatzplanHaeH'

    def ready(self):
        import PersonaleinsatzplanHaeH.signals