from django.apps import AppConfig


class PartslogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partslog'

    def ready(self):
        import partslog.signals
