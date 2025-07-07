from rest_framework import serializers

from crud_functionality.referral_system_database.models import Hospital, MedicalServiceUnit

class HospitalSerializer(serializers.ModelSerializer):
    medical_service_unit = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MedicalServiceUnit.objects.all(),
        required=False
    )

    class Meta:
        model = Hospital
        fields = [
            'id', 'hospital_name', 'hospital_id', 'hospital_type', 'setting',
            'contact_number', 'email', 'picture', 'hospital_description',
            'ownership', 'empanelments', 'org_facility_id', 'state',
            'district', 'block', 'city_or_village', 'address', 'geo_lat',
            'geo_long', 'geo_alt', 'status', 'higher_facility',
            'delivery_point', 'medical_service_unit', 'training_institure',
            'fru', 'sncu', 'nbsu'
        ]

    def create(self, validated_data):
        msu_data = validated_data.pop('medical_service_unit', [])
        hospital = Hospital.objects.create(**validated_data)
        hospital.medical_service_unit.set(msu_data)
        return hospital

    def update(self, instance, validated_data):
        msu_data = validated_data.pop('medical_service_unit', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if msu_data is not None:
            instance.medical_service_unit.set(msu_data)
        return instance