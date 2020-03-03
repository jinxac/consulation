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

from office.views import OfficeList, OfficeDetail
from assistant.views import AssistantList, AssistantDetail
from appointment.views import AppointmentAssistantList, \
    AppointmentAssistantDetail, \
    AppointmentDoctorList, \
    AppointmentDoctorDetail, \
    UploadRecordView

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
    path('api/v0/offices/', OfficeList.as_view(), name='offices'),
    path('api/v0/offices/<int:pk>/', OfficeDetail.as_view(), name='office'),
    path('api/v0/assistants/', AssistantList.as_view(), name='assistants'),
    path('api/v0/assistants/<int:pk>/', AssistantDetail.as_view(), name='assistant'),
    path('api/v0/appointments-assistant/', AppointmentAssistantList.as_view(), name='appointments_assistant'),
    path('api/v0/appointments-assistant/<int:pk>', AppointmentAssistantDetail.as_view(), name='appointment_assistant'),
    path('api/v0/appointments-doctor/', AppointmentDoctorList.as_view(), name='appointments_doctor'),
    path('api/v0/appointments-doctor/<int:pk>', AppointmentDoctorDetail.as_view(), name='appointment_doctor'),
    path('api/v0/add-record/', UploadRecordView.as_view(), name='add_record')
]
