# backend/apps/ai_integration/urls.py
from django.urls import path
from django.http import HttpResponse

# Заглушка для ai_integration
def ai_placeholder(request):
    return HttpResponse("AI Integration module placeholder")

urlpatterns = [
    path('', ai_placeholder, name='ai_placeholder'),
]