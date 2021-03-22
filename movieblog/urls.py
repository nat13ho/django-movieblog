from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from movieblog.apps.posts.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('posts/', include('movieblog.apps.posts.urls')),
    path('profiles/', include('movieblog.apps.profiles.urls')),
    path('accounts/', include('movieblog.apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
