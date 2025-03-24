from django.urls import path
from .views import chatbot, get_response

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("get-response/", get_response, name="chat_response"),
]
