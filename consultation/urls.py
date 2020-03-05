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
from django.conf.urls import include, url


from doctor.views import DoctorList, DoctorDetail
from client.views import ClientList, ClientDetail
from authservice.views import UserSignupView

from office.views import OfficeList, OfficeDetail
from assistant.views import AssistantList, AssistantDetail
from appointment.views import AppointmentList, \
    AppointmentDetail, \
    UploadRecordView, \
    DoctorShareRecordList, \
    DoctorShareRecordDetail, \
    get_appointment_records, \
    revoke_record_access, \
    FeedbackList, \
    FeedbackDetail

from rest_framework_simplejwt import views as jwt_views

from rest_framework import routers
router = routers.DefaultRouter()
router.register('clients/add-record', UploadRecordView, basename='cutareadel')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v0/register/', UserSignupView.as_view(), name='register'),

    # Doctor
    path('api/v0/doctors/', DoctorList.as_view(), name='doctors'),
    path('api/v0/doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor'),

    # Client
    path('api/v0/clients/<int:pk>/', ClientDetail.as_view(), name='client'),
    path('api/v0/clients/revoke-record/', revoke_record_access, name='revoke-record'),
    path('api/v0/clients/share-records/', DoctorShareRecordList.as_view(), name='share_records'),
    path('api/v0/clients/share-records/<int:pk>', DoctorShareRecordDetail.as_view(), name='share_record'),

    # Office
    path('api/v0/offices/', OfficeList.as_view(), name='offices'),
    path('api/v0/offices/<int:pk>/', OfficeDetail.as_view(), name='office'),

    # Assistant
    path('api/v0/assistants/', AssistantList.as_view(), name='assistants'),
    path('api/v0/assistants/<int:pk>/', AssistantDetail.as_view(), name='assistant'),

    # Appointment
    path('api/v0/appointments/', AppointmentList.as_view(), name='appointments'),
    path('api/v0/appointments/<int:pk>', AppointmentDetail.as_view(), name='appointment'),
    path('api/v0/appointments/<int:pk>/records/', get_appointment_records, name='appointment_records'),
    path('api/v0/feedback/', FeedbackList.as_view(), name='feedback_list'),
    path('api/v0/feedback/<int:pk>/', FeedbackDetail.as_view(), name='feedback'),

    # Records
    url(r'^api/v0/', include(router.urls)),
]
