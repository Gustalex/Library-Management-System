from django.apps import AppConfig

class BookServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_services'
    
    def ready(self):
        import book_services.signals
