from django.urls import path  # Changed import statement

from . import views

app_name = 'register'
urlpatterns = [
    path('register/', views.register, name='register'),  # Updated URL pattern
    path('login/', views.signin, name='login'),  # Updated URL pattern
    path('signout/', views.signout, name='logout'),  # Updated URL pattern
    path('profile/', views.profile, name='profile'),  # Updated URL pattern
    path('profile_pic/', views.profile_pic, name='profile_pic'),  # Updated URL pattern
    path('comments/<str:pk>/', views.comment, name='comment'),  # Updated URL pattern
]
