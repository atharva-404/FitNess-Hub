from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import GymUser

# Registration Form
class GymRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = GymUser
        fields = ['name', 'number', 'email', 'password', 'age', 'weight', 'height', 'gender']

# Login Form
class GymLoginForm(forms.Form):
    username = forms.EmailField()  # Username is the email
    password = forms.CharField(widget=forms.PasswordInput())  # Password field

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not GymUser.objects.filter(email=username).exists():
            raise forms.ValidationError('No user found with this email.')
        return username
    

# Contact Form
class ContactUs(forms.Form):
    name=forms.CharField()
    email = forms.EmailField()  # email 
    mobno=forms.CharField()
    msg = forms.CharField()  # message field



FITNESS_GOALS = [
    ('weight_gain', 'Weight Gain'),
    ('weight_loss', 'Weight Loss'),
    ('muscle_gain', 'Muscle Gain'),
]

class TrainerSelectionForm(forms.Form):
    trainer = forms.ModelChoiceField(queryset=GymUser.objects.all(), widget=forms.RadioSelect)
    fitness_goal = forms.ChoiceField(choices=FITNESS_GOALS, widget=forms.RadioSelect)



class GymUserProfileForm(forms.ModelForm):
    class Meta:
        model = GymUser
        fields = ['name', 'number', 'email', 'age', 'weight', 'height', 'gender', 'goal', 'plan', 'trainer']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'plan': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'goal': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
        }
