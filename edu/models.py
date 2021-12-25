from django.db import models

# Create your models here.

class course(models.Model):
    cors_id = models.AutoField(primary_key=True)
    cors_cat = models.CharField(max_length=100)
    cors_name = models.CharField(max_length=100)
    cors_full = models.CharField(max_length=150)
    cors_dur = models.CharField(max_length=20)
    cors_detail = models.CharField(max_length=250)
    cors_pack = models.CharField(max_length=5)

    def __str__(self):
        return self.cors_name


class student(models.Model):
    std_id = models.AutoField(primary_key=True)
    reg_year = models.CharField(max_length=10)
    reg_mon = models.CharField(max_length=10)
    session_year = models.CharField(max_length=10)
    session_month = models.CharField(max_length=10)
    reg_no = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    father = models.CharField(max_length=150)
    mother = models.CharField(max_length=150)
    dob = models.DateField()
    address = models.CharField(max_length=250)
    contact = models.CharField(max_length=15)
    category = models.CharField(max_length=25)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    lpc = models.CharField(max_length=50)
    passing_year = models.CharField(max_length=10)
    board = models.CharField(max_length=100)
    gread = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='edu/images')
    dor = models.DateField(auto_now_add=True)

    enroll_number = models.CharField(max_length=50)
    cretificate_no = models.CharField(max_length=100)

    theory_s1 = models.CharField(max_length=100)
    os_s1 = models.CharField(max_length=100)
    pretical_s1 = models.CharField(max_length=100)
    theory_s2 = models.CharField(max_length=100)
    pretical_s2 = models.CharField(max_length=100)
    oral_s2 = models.CharField(max_length=100)

    is_registerd = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)
    is_examinee = models.BooleanField(default=False)
    is_certified = models.BooleanField(default=False)

    def __str__(self):
        return self.name