from django.shortcuts import render
from rest_framework.response import Response

from app.models import Student
from crud_functionality.app.serializers import StudentSerializer

