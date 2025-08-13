from django.contrib import admin
from django.urls import path, include
from analytics import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('analytics.urls')),
    path('', views.home, name='home'),
]
