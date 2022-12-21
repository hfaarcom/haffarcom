from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('MainAdmin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('Admin/', include('Admin.urls')),
    path('', include('allauth.urls'))
]
