from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('user/<str:pk>/', views.user_view, name='user-view'),  # Changed <w+> to <str:pk> for string matching
    path('search/', views.search, name='search'),
    path('stats/', views.stats, name='stats'),
    path('fetch-products-with-pagination/', views.fetch_products_with_pagination, name='fetch_products_with_pagination'),
    path('get-total-products/', views.get_total_products, name='get_total_products'),
    path('chat/', views.chat, name='chat'),
]
