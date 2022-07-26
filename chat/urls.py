from django.contrib import admin
from django.urls import path

from . import views

from django.contrib.auth import views as auth_views
app_name = 'chat'

urlpatterns = [
    path('start_chat/', views.private_chat_room_view, name="start_chat"),
    path('create_or_return_private_chat/', views.create_or_return_private_chat, name='create-or-return-private-chat'), # TODO: ADD THIS LINE.
    path('start_new_chat/<int:id>', views.start_new_chat, name="start_new_chat"),
]