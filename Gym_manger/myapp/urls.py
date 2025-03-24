from django.urls import path
from myapp import views
from django.urls import path
from .views import generate_otp, login_view, logout_view, register, verify_otp

urlpatterns = [
  path('',views.Homepage,name='userpage'),
  path("home/", views.home_view, name="home"),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),

  path('generate_otp/', generate_otp, name='generate_otp'),
  path('verify_otp/', verify_otp, name='verify_otp'),
  path('register/', register, name='register'),

  path('protin/',views.protin,name='protin'),

  path('subscription/', views.subscription_page, name='subscription'),
  path('process-payment/',views. process_payment, name='process_payment'),
  path('payment-success/', views.payment_success, name='payment_success'),

  path('workout-videos/', views.workout_videos, name='workout_videos'),
  path('premium/', views.premium, name='premium'),
  
  path('trainer-dash/', views.trainerdash, name='trainer-dash'),
  path('send-message/', views.send_message, name='send_message'),
  path('contact-mail/', views.home_view, name='contact_mail'),
  path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
 path('profile/', views.profile_view, name='profile'),]

  


