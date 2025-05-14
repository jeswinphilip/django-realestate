from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Changed to user_login
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_properties/', views.user_properties, name='user_properties'),
    path('logout/', views.logout_view, name='logout'),
    path('property/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('property/image/delete/<int:image_id>/', views.delete_property_image, name='delete_property_image'),
    path('property/<int:property_id>/delete/', views.delete_property, name='delete_property'),
]