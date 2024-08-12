from django.apps import AppConfig


class FineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fine'
    
    def ready(self):
        import fine.signals