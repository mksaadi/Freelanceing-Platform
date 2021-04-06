from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path("<int:user_id>/", views.chatroom, name='chatroom'),
    path("ajax/<int:user_id>/", views.ajax_load_messages, name="chatroom-ajax"),
]