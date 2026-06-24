from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ai-assistant/', views.ai_assistant, name='ai_assistant'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/contact/', views.contact_api, name='contact_api'),
    path('resume/', views.resume, name='resume'),
]
