from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import UserRegistrationForm
from .models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from properties.models import Property
from properties.forms import PropertyForm
from properties.models import PropertyImage
from django.contrib import messages
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Changed from login to auth_login
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):  # Changed function name from login to user_login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Changed from login to auth_login
            return redirect('user_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')


#dashboard view

User = get_user_model()  # Get your custom User model
@login_required
def user_dashboard(request):
 
    # Get user details
    user = request.user
    
    
    # Get user's properties or other relevant data
    # user_properties = Property.objects.filter(user=user)

    return render(request, 'accounts/user_dashboard.html', {'user': user})

#logout view

def logout_view(request):
    logout(request)
    return redirect('login')

def user_properties(request):
    user = request.user
    user_properties = Property.objects.filter(user=user)
    return render(request, 'accounts/user_property.html', {'user_properties': user_properties})

@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            # Save updated property
            updated_property = form.save(commit=False)
            
            # Only update district and area if provided
            district = form.cleaned_data.get('district')
            area = form.cleaned_data.get('area')
            
            if district and area:
                # Update location if provided
                updated_property.district = district
                updated_property.area = area
            
            updated_property.save()
            
            # Handle images
            if request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property=updated_property, image=image)
            
            messages.success(request, 'Property updated successfully!')
            return redirect('user_properties')
    else:
        form = PropertyForm(instance=property)

    # Get existing images for the property
    existing_images = PropertyImage.objects.filter(property=property)

    return render(request, 'accounts/edituser_property.html', {
        'form': form,
        'property': property,
        'existing_images': existing_images
    })
@login_required
def delete_property_image(request, image_id):
    """
    View to delete a specific property image
    """
    image = get_object_or_404(PropertyImage, id=image_id, property__user=request.user)
    property_id = image.property.id

    image.delete()
    messages.success(request, 'Image deleted successfully!')

    return redirect('edit_property', property_id=property_id)

# In your views.py
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property has been successfully deleted.')
        return redirect('user_properties')
    
    return render(request, 'accounts/confirm_delete_property.html', {'property': property})

