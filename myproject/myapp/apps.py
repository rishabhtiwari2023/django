from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        import myapp.signals

    default_auto_field = 'django.db.models.BigAutoField'
