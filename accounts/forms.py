from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Phone number must be 10 digits starting with 6, 7, 8, or 9 (Indian format)."
            )
        ]
    )
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the default widgets for password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check username length
        if len(username) < 4:
            raise ValidationError("Username must be at least 4 characters long.")
        
        # Check for alphanumeric characters
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
            
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use another email or login.")
            
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        # Check that name contains only letters
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise ValidationError("Name can only contain letters and spaces.")
            
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        # Check that name contains only letters
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise ValidationError("Name can only contain letters and spaces.")
            
        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        # If phone number is provided, validate its format
        if phone_number:
            # Check for existing phone number
            if User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError("This phone number is already registered.")
                
        return phone_number
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        
        # Additional password validation
        if password2:
            # Check length
            if len(password2) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
                
            # Check for at least one digit
            if not re.search(r'\d', password2):
                raise ValidationError("Password must contain at least one digit.")
                
            # Check for at least one uppercase letter
            if not re.search(r'[A-Z]', password2):
                raise ValidationError("Password must contain at least one uppercase letter.")
                
            
        return password2