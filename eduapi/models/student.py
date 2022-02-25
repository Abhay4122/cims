from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    father = models.CharField(max_length=150)
    mother = models.CharField(max_length=150)
    dob = models.DateField()
    address = models.CharField(max_length=250)
    contact = models.CharField(max_length=20)
    category = models.CharField(max_length=25)
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    lpc = models.CharField(max_length=50)
    passing_year = models.CharField(max_length=10)
    board = models.CharField(max_length=100)
    gread = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='edu/images', blank=True, null=True)

    reg_year = models.CharField(max_length=10, blank=True, null=True)
    reg_mon = models.CharField(max_length=10, blank=True, null=True)
    session_year = models.CharField(max_length=10, blank=True, null=True)
    session_month = models.CharField(max_length=10, blank=True, null=True)
    dor = models.DateField(auto_now_add=True)

    enroll_number = models.CharField(max_length=50, blank=True, null=True)
    cretificate_no = models.CharField(max_length=100, blank=True, null=True)

    theory_s1 = models.CharField(max_length=100, blank=True, null=True)
    os_s1 = models.CharField(max_length=100, blank=True, null=True)
    pretical_s1 = models.CharField(max_length=100, blank=True, null=True)
    theory_s2 = models.CharField(max_length=100, blank=True, null=True)
    pretical_s2 = models.CharField(max_length=100, blank=True, null=True)
    oral_s2 = models.CharField(max_length=100, blank=True, null=True)

    is_registerd = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)
    is_examinee = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)

    def __str__(self):
        return self.name