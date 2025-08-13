
from django.urls import path
from . import views
urlpatterns = [
    path('general/', views.general_dashboard, name='general_dashboard'),
    path('users/', views.user_analytics, name='user_analytics'),
    path('videos/', views.video_analytics, name='video_analytics'),
]
