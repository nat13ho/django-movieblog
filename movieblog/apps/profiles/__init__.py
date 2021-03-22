from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'movieblog.apps.profiles'
    verbose_name = 'Profiles'

    def ready(self):
        import movieblog.apps.profiles.signals


default_app_config = 'movieblog.apps.profiles.ProfilesConfig'
