from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    roll_no = serializers.IntegerField(unique=True)
    city = serializers.CharField(max_length=255)
    status = serializers.BooleanField(default=False)