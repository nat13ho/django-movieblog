from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
    path('<int:post_id>/comments/add/', views.add_comment, name='comment_add'),
    path('<int:post_id>/comments/<int:comment_id>/remove', views.remove_comment, name='comment_remove'),
]