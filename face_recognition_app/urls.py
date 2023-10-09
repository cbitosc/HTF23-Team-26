from django.urls import path
from . import views

urlpatterns = [
    path('facial_scan/', views.facial_scan, name='facial_scan'),
    path('courses/',views.courses,name='courses'),
    path('', views.homepage, name='homepage'),
    path('attendance/',views.attendance,name='attendance'),
    path('',views.login, name='login')

]
