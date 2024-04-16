from django.apps import AppConfig


class TemoignageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'temoignage'

    def ready(self):
        import temoignage.models  # Import your models module