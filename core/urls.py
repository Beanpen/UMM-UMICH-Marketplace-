from django.contrib import admin
from django.urls import path, include  # Changed import statement
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Updated URL pattern
    path('accounts/', include('register.urls')),  # Updated URL pattern
    path('products/', include('products.urls')),  # Updated URL pattern
    path('homepage/', include('homepage.urls')),  # Updated URL pattern
]

urlpatterns += [
    path('', RedirectView.as_view(url='/homepage/', permanent=True), name='home'),  # Updated URL pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
