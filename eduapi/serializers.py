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
            'id', 'name', 'gender', 'father', 'mother', 'aadhar', 'dob', 'address', 'contact',
            'category', 'course', 'lpc', 'passing_year', 'board', 'gread', 'photo', 'reg_year',
            'reg_mon', 'session_year', 'session_month', 'is_registerd'
        )


# Student serializer for add update
class StudentWithoutPhotoSerializer(serializers.ModelSerializer):
    # course = serializers.RelatedField(many=False, read_only=True)
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'gender', 'father', 'mother', 'aadhar', 'dob', 'address',
            'contact', 'category', 'course', 'lpc', 'passing_year', 'board', 'gread',
            'reg_year', 'reg_mon', 'session_year', 'session_month', 'is_registerd'
        )


# Student serializer for list view
class StudentListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    admission_session = serializers.SerializerMethodField()

    def get_admission_session(self, obj):
        return f"{obj.reg_mon} - {obj.reg_year} to {obj.session_month} - {obj.session_year}"
    
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'father', 'course', 'admission_session', 'enroll_number'
        )


# Student serializer for detail view
class StudentDetailSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'gender', 'father', 'mother', 'aadhar', 'dob', 'address', 'contact',
            'category', 'course', 'lpc', 'passing_year', 'board', 'gread', 'photo', 'reg_year',
            'reg_mon', 'session_year', 'session_month', 'enroll_number', 'cretificate_no'
        )


# Get enroll detail of student
class EnrollDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    admission_session = serializers.SerializerMethodField()

    def get_admission_session(self, obj):
        return f"{obj.reg_mon.split('_')[0]} - {obj.reg_year} to {obj.session_month.split('_')[0]} - {obj.session_year}"
    
    # reg_mon = serializers.CharField(source='person_id')

    class Meta:
        model = Student
        fields = (
             'id', 'name', 'father', 'course', 'contact', 'admission_session', 'enroll_number'
        )


# Examinee Student serializer for list view
class StudentExamineeListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    th1 = serializers.SerializerMethodField('get_th1')
    pr1 = serializers.SerializerMethodField('get_pr1')
    or1 = serializers.SerializerMethodField('get_or1')
    th2 = serializers.SerializerMethodField('get_th2')
    pr2 = serializers.SerializerMethodField('get_pr2')
    or2 = serializers.SerializerMethodField('get_or2')

    def get_th1(self, obj):
        return obj.theory_s1

    def get_pr1(self, obj):
        return obj.pretical_s1

    def get_or1(self, obj):
        return obj.oral_s1

    def get_th2(self, obj):
        return obj.theory_s2

    def get_pr2(self, obj):
        return obj.pretical_s2

    def get_or2(self, obj):
        return obj.oral_s2
    
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'course', 'enroll_number', 'cretificate_no', 'is_certified',
            'th1', 'pr1', 'or1', 'th2', 'pr2', 'or2', 'os'
        )


# Examinee Student detail serializer for list view
class StudentADCAExamineeDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    admission_session = serializers.SerializerMethodField()

    def get_admission_session(self, obj):
        return f"{obj.reg_mon} - {obj.reg_year} to {obj.session_month} - {obj.session_year}"
    
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'father', 'course', 'admission_session', 'enroll_number', 'cretificate_no',
            'theory_s1', 'os', 'pretical_s1', 'theory_s2', 'pretical_s2', 'oral_s2', 'exam_year', 'exam_month'
        )


# Examinee Student detail serializer for list view
class StudentDCAExamineeDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=False)
    admission_session = serializers.SerializerMethodField()

    def get_admission_session(self, obj):
        return f"{obj.reg_mon} - {obj.reg_year} to {obj.session_month} - {obj.session_year}"
    
    class Meta:
        model = Student
        fields = (
            'id', 'name', 'father', 'course', 'admission_session', 'enroll_number', 'cretificate_no',
            'theory_s1', 'pretical_s1', 'oral_s1', 'exam_year', 'exam_month'
        )
