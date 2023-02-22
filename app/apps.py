from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Blog management'
