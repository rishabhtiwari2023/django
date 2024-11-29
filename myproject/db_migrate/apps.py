from django.apps import AppConfig


class DbMigrateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db_migrate'
