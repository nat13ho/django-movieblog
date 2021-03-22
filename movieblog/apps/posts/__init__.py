from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'movieblog.apps.posts'
    verbose_name = 'Posts'

    def ready(self):
        import movieblog.apps.posts.signals


default_app_config = 'movieblog.apps.posts.PostsConfig'
