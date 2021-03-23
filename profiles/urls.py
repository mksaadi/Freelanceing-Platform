from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
# path('login/', views.user_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# change password urls
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
# reset password urls
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),
    path('posts/', include("posts.urls", namespace='posts')),
    path('register_freelancer/', views.register_freelancer, name='register_freelancer'),
    path('register_client/', views.register_client, name='register_client'),
    path('register/', views.register, name='register'),
    path('<int:user_id>/', views.profile_view, name='profile_view'),
    path('ajax/load-skills/', views.load_skills, name='load_skills'),
    path('connection_request_view/', views.connection_request_view, name='connection_request_view'),
    path('profiles_list_view/', views.ProfileListView.as_view(), name='profiles_list_view'),
    path('send_connection/', views.send_connection, name='send_connection'),
    path('remove_connection/', views.remove_connection, name='remove_connection'),
    path('approve_connection/', views.approve_connection, name='approve_connection'),
    path('connection_list/', views.connection_list, name='connection_list'),
    path('<int:id>/ProfileDetailView/', views.ProfileDetailView.as_view(), name='ProfileDetailView'),
]