from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>/', views.ProfileView.as_view(), name='profile_details'),
    path('<int:pk>/update/', views.update_profile, name='profile_update'),
    path('bookmarks/', views.FavouritePostListView.as_view(), name='bookmarks'),
    path('bookmarks/<int:post_id>/add/', views.add_to_bookmarks, name='bookmark_add'),
    path('bookmarks/<int:post_id>/remove/', views.remove_from_bookmarks, name='bookmark_remove'),
]