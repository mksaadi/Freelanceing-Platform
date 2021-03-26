from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list_view, name='post_view'),
    path('find_jobs/', views.find_jobs, name='find_jobs'),
    path('like_unlike', views.like_unlike_view, name='like_unlike'),
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post-update'),

]