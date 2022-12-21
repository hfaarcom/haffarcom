from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('MainAdmin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', include('Admin.urls')),
    path('', include('allauth.urls'))
]
