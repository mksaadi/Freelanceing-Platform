from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list_view, name='post_view'),
    path('job_list_view/', views.job_list_view, name='job_list_view'),
    path('find_jobs/', views.find_jobs, name='find_jobs'),
    path('like_unlike', views.like_unlike_view, name='like_unlike'),
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('send_request/', views.send_request, name='send_request'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail_view'),

]