from django.db.models import fields
from rest_framework import serializers

from .models import *


# Course all perpose
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'cors_cat', 'cors_name', 'cors_full', 'cors_dur', 'cors_detail', 'cors_pack')


# Student selected fields
class StudentSelectedFieldsSerializer(serializers.ModelSerializer):
    # course = serializers.RelatedField(many=False, read_only=True)
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'gender', 'father', 'mother', 'dob', 'address', 'contact', 'category',
            'course', 'lpc', 'passing_year', 'board', 'gread', 'photo', 'reg_year', 'reg_mon',
            'session_year', 'session_month', 'enroll_number', 'dor'
        )


# Student all fields
class StudentAllFiedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
