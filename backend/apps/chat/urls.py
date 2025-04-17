# backend/apps/chat/urls.py
from django.urls import path
from django.http import HttpResponse

# Заглушка для приложения chat
def chat_placeholder(request):
    return HttpResponse("Chat module placeholder")

urlpatterns = [
    path('', chat_placeholder, name='chat_placeholder'),
]