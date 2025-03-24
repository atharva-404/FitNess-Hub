from django.urls import path
from .views import ai_trainer

urlpatterns = [
    path('ai-trainer/', ai_trainer, name='ai_trainer'),
]
