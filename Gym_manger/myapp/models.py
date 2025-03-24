from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Custom User Manager
class GymUserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, name, mobile, password):
        user = self.create_user(email, name, mobile, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
class GymUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    subscription=models.BooleanField(default=False)
    plan=models.CharField(max_length=100,default="noplan")
    trainer=models.ForeignKey('self',default=None, on_delete=models.SET_NULL, null=True, blank=True)
    goal=models.CharField(default='',max_length=100)
    objects = GymUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField(default=0)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.plan} - {'Paid' if self.payment_status else 'Pending'}"
from django.utils import timezone

created_at = models.DateTimeField(default=timezone.now)  # Instead of auto_now_add=True



class WorkoutVideo(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    video_url = models.URLField()  # Link to YouTube or video file
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TrainerMessage(models.Model):
    trainer = models.ForeignKey(GymUser, on_delete=models.CASCADE, related_name="received_messages")
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE, related_name="sent_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.name} to {self.trainer.name} at {self.timestamp}"