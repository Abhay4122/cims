from django.db.models import fields
from rest_framework import serializers

from .models import *


# Course all perpose
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_category', 'course_name', 'course_full_form', 'course_duration', 'course_detail', 'course_package')


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_category', 'course_name', 'course_duration', 'course_package')


# Student serializer for add update
class StudentSerializer(serializers.ModelSerializer):
    # course = serializers.RelatedField(many=False, read_only=True)
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'gender', 'father', 'mother', 'dob', 'address', 'contact', 'category',
            'course', 'lpc', 'passing_year', 'board', 'gread', 'photo', 'reg_year', 'reg_mon',
            'session_year', 'session_month', 'enroll_number', 'dor'
        )


# Student serializer for list view
class StudentListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    admission_session = serializers.SerializerMethodField()

    def get_admission_session(self, obj):
        return f"{obj.reg_mon.split('_')[0]} - {obj.reg_year} to {obj.session_month.split('_')[0]} - {obj.session_year}"
    
    # reg_mon = serializers.CharField(source='person_id')

    class Meta:
        model = Student
        fields = (
             'id', 'name', 'father', 'course', 'admission_session', 'enroll_number'
        )


# Student serializer for detail view
class StudentDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'gender', 'father', 'mother', 'dob', 'address', 'contact', 'category',
            'course', 'lpc', 'passing_year', 'board', 'gread', 'photo', 'reg_year', 'reg_mon',
            'session_year', 'session_month', 'enroll_number', 'dor'
        )
