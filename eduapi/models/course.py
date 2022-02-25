from django.db import models

# Create your models here.

class Course(models.Model):
    course_category = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    course_full_form = models.CharField(max_length=150)
    course_duration = models.CharField(max_length=20)
    course_detail = models.CharField(max_length=250, blank=True, null=True)
    course_package = models.CharField(max_length=5)

    def __str__(self):
        return self.course_name