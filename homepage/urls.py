from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('user/<str:pk>/', views.user_view, name='user-view'),  # Changed <w+> to <str:pk> for string matching
    path('search/', views.search, name='search'),
    path('stats/', views.stats, name='stats'),
]
