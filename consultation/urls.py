"""consultation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from doctor.views import DoctorList, DoctorDetail
from client.views import ClientList, ClientDetail
from authservice.views import UserSignupView

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v0/doctors/', DoctorList.as_view(), name='doctors'),
    path('api/v0/doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor'),
    path('api/v0/clients/', ClientList.as_view(), name='clients'),
    path('api/v0/clients/<int:pk>/', ClientDetail.as_view(), name='client'),
    path('api/v0/register/', UserSignupView.as_view(), name='register'),
]
