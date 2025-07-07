from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crud_functionality.referral_system_database.views import HospitalViewSet

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]