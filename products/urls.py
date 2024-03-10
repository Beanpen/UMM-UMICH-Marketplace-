from django.urls import path  # Changed import statement

from . import views

app_name = 'products'
urlpatterns = [
    path('post/', views.post, name='post'),  # Updated URL pattern
    # path('order/', views.order, name='order'),  # Commented out deprecated URL pattern
    path('details/<int:pk>/', views.details, name='details'),  # Updated URL pattern
    path('order/<int:pk>/', views.order, name='order'),  # Updated URL pattern
    path('update/<int:pk>/', views.update, name='update'),  # Updated URL pattern
    path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),  # Updated URL pattern
]
