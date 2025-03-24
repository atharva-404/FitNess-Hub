from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from myapp.models import GymUser
from myapp.forms import GymLoginForm,ContactUs  # Your login form
from myapp.mailsend import otpsender, responseMail
from .models import TrainerMessage, WorkoutVideo
import random
from django.contrib.auth.hashers import make_password
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import GymRegistrationForm, GymLoginForm, GymUserProfileForm, TrainerSelectionForm
from .models import GymUser
from django.contrib.auth import get_user_model

def Homepage(request):
    form = GymLoginForm()  # Make sure this is defined
    return render(request, 'index.html', {'form': form})


def subscription_page(request):
    if request.session.session_key==None:
        return  redirect("userpage")
   
    return render(request, 'subscription.html')


def home_view(request):
    if request.session.session_key==None:
        return  redirect("userpage")
    user = GymUser.objects.get(email=request.session.get("email"))
    if user.subscription==False:
        return redirect("subscription")

    if request.method == "POST":
        form = ContactUs(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            mobno = form.cleaned_data["mobno"]
            msg = form.cleaned_data["msg"]
            
            print(name, email, mobno, msg)  # Debugging
            
        try:
            responseMail(name, email, mobno, msg)
            return JsonResponse({"success": True, "message": "Response sent successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": "Failed to send mail"}, status=500)


    trainers = GymUser.objects.filter(is_admin=True)  # Assuming trainers are admins
    return render(request, 'home.html', {'trainers': trainers})

def protin(request):
    if request.session.session_key==None:
        return  redirect("userpage")
    return render(request,'protin.html')


# Registration View
otp_storage = {}
from django.core.cache import cache
def generate_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        otp = str(otpsender(email,request.POST.get('name')))  # Generate OTP
        #otp = otpsender(email, name)
        cache.set(email, otp, timeout=300)  # Store OTP for 5 minutes

        print(f"OTP for {email}: {otp}")  # Debugging purpose (remove in production)

        return JsonResponse({"message": "OTP sent successfully!"})

def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        stored_otp = cache.get(email)  # Retrieve OTP from cache
        if stored_otp and stored_otp == otp:
            request.session['verified_email'] = email  # Store verified email
            return JsonResponse({"success": True, "message": "OTP Verified!"})
        else:
            return JsonResponse({"success": False, "error": "Invalid OTP or expired OTP"})
        
        
def register(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)  # Debugging
        
        form = GymRegistrationForm(request.POST)
        
        if form.is_valid():
            email = request.session.get('verified_email')
            if not email:
                return JsonResponse({"error": "Email not verified"}, status=400)

            # Hash the password
            password = make_password(form.cleaned_data['password'])

            # Save user
            gym_user = GymUser.objects.create(
                name=form.cleaned_data['name'],
                number=form.cleaned_data['number'],
                email=email,  # Use verified email from session
                password=password,
                height=form.cleaned_data['height'],
                weight=form.cleaned_data['weight'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender']
            )

            print("User saved successfully!")  # Debugging
            del request.session['verified_email']  # Clear session after successful registration

            return JsonResponse({"success": True, "message": "Registration Successful!"})
        
        else:
            print("Form errors:", form.errors)  # Debugging
            return JsonResponse({"error": form.errors}, status=400)

    return render(request, 'register.html', {'form': GymRegistrationForm()})



def login_view(request):
    if request.method == "POST":
        form = GymLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = GymUser.objects.get(email=email)  # Fetch user from GymUser model
                
                if user.check_password(password):  # Validate password
                    login(request, user)  # Log in the user
                    request.session["email"] = email
                    request.session["name"] = user.name
                    request.session["number"] = user.number
                    
                    # Redirect based on role
                    redirect_url = "trainer-dash" if user.is_admin == 1 else "home"
                    
                    return JsonResponse({"status": "success", "redirect_url": redirect_url})
                
                else:
                    return JsonResponse({"status": "error", "message": "Incorrect password."})
            
            except GymUser.DoesNotExist:
                return JsonResponse({"status": "error", "message": "No user found with this email."})
        
        # Form validation errors
        return JsonResponse({"status": "error", "message": "No user found with this email."})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
        



# Logout View
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect("userpage")



import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Subscription

# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=('rzp_live_7owtDrVKyiULSB','AQivNa1NJFsBQYqz1yTe1KMt'))


@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = request.session.get("name")
        email = request.session.get("email")
        plan = data.get("plan")
        print(name,email,)

        prices = {"basic": 10, "standard": 1, "premium": 1}
        amount = prices.get(plan, 0) * 100  # Convert to paise

        # Create Razorpay Order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        }
        order = razorpay_client.order.create(data=order_data)

        # Save Subscription in Database
        subscription = Subscription.objects.create(
            name=name, 
            email=email, 
            plan=plan, 
            order_id=order["id"]  # Ensure order_id is correctly added
        )

        return JsonResponse({"key": settings.RAZORPAY_KEY_ID, "order_id": order["id"]})

    return JsonResponse({"error": "Invalid Request"}, status=400)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        prices = {"basic": 10, "standard": 1, "premium": 1}


        # Update Subscription Status
        try:
            subscription = Subscription.objects.get(order_id=order_id)
            subscription.payment_status = True
            subscription.amount=prices[subscription.plan]
            user=GymUser.objects.get(email=subscription.email)
            user.subscription=True
            user.plan=subscription.plan
            user.save()
            subscription.save()
            redirect_url = "/premium/" if subscription.plan.lower() == "premium" else "/home/"
            return JsonResponse({"message": "Payment Successful!", "success": True, "redirect_url": redirect_url})
        
        except Subscription.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=400)

    return JsonResponse({"error": "Invalid Request"}, status=400)


def workout_videos(request):
    category = request.GET.get('category', None)
    videos = WorkoutVideo.objects.all()
    if category:
        videos = videos.filter(category=category)
    return render(request, 'workout_videos.html', {'videos': videos})


def premium(request):
    users = GymUser.objects.filter(is_admin=1)  # Error if duplicates exist

    print(users)

    if request.method == "POST":
        form = TrainerSelectionForm(request.POST)
        if form.is_valid():
            selected_trainer = form.cleaned_data['trainer']
            fitness_goal = form.cleaned_data['fitness_goal']
            user = GymUser.objects.get(email=request.session.get('email'))
            user.trainer=selected_trainer
            user.goal=fitness_goal
            user.save()
            
            # Handle form submission (save to DB, send email, etc.)
            return redirect('home')  # Redirect after submission
    else:
        form = TrainerSelectionForm()
    
    return render(request, 'premium.html', {'trainers': users, 'form': form})

def trainerdash(request):
    premium_users = GymUser.objects.filter(subscription=True,plan='premium')
    messages = TrainerMessage.objects.all().order_by('-timestamp')
    # Get messages from premium users
    context = {
        'premium_users': premium_users,
        'messages': messages
    }

    return render(request, 'trainer-dash.html', context)

def delete_message(request, message_id):
    message = get_object_or_404(TrainerMessage, id=message_id)
    message.delete()
    return redirect('trainer-dash')  # Redirect back to trainer dashboard


def send_message(request):
    if request.method == "POST":
        trainer_id = request.POST.get("trainer_id")
        message_text = request.POST.get("message")

        if trainer_id and message_text:
            trainer = GymUser.objects.filter(id=trainer_id).first()
            user = GymUser.objects.get(email=request.session.get("email"))  # Fetch user from session

            if trainer:
                TrainerMessage.objects.create(user=user, trainer=trainer, message=message_text)
                return JsonResponse({"success": True, "message": "Message sent successfully!"})

        return JsonResponse({"success": False, "message": "Invalid trainer or message."})

    return render(request, "home.html")



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GymRegistrationForm

from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

def profile_view(request):
    if request.session.session_key==None:
        return  redirect("userpage")
    user = GymUser.objects.get(email=request.session.get("email"))
    trainers = GymUser.objects.filter(is_admin=True)

    if request.method == "POST":
        # Update Profile Information
        user.name = request.POST.get("name")
        user.number = request.POST.get("number")
        user.age = request.POST.get("age")
        user.weight = request.POST.get("weight")
        user.height = request.POST.get("height")
        user.gender = request.POST.get("gender")
        user.goal = request.POST.get("goal")

        # Trainer Assignment
        trainer_id = request.POST.get("trainer")
        if trainer_id:
            user.trainer = GymUser.objects.filter(id=trainer_id).first()

        # Password Change Logic
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if current_password and new_password and confirm_password:
            if check_password(current_password, user.password):
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    messages.success(request, "Password updated successfully.")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Current password is incorrect.")
        
        user.save()
        return redirect("profile")

    return render(request, "profile.html", {"user": user, "trainers": trainers})
