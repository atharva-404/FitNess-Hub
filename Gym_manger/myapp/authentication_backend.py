from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from myapp.models import GymUser  # Import your custom user model

class GymUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = GymUser.objects.get(email=username)  # Check by email
            if user.check_password(password):  # Ensure password matches
                return user
        except GymUser.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return GymUser.objects.get(pk=user_id)
        except GymUser.DoesNotExist:
            return None
