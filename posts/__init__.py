from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        import posts.signals


default_app_config = 'posts.PostsConfig'
