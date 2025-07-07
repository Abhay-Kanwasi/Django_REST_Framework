from rest_framework import viewsets

from crud_functionality.referral_system_database.models import Hospital
from crud_functionality.referral_system_database.serializers.model_serializers import HospitalSerializer

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer