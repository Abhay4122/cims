from django.db import models

# Create your models here.

class Course(models.Model):
    cors_cat = models.CharField(max_length=100)
    cors_name = models.CharField(max_length=100)
    cors_full = models.CharField(max_length=150)
    cors_dur = models.CharField(max_length=20)
    cors_detail = models.CharField(max_length=250, blank=True, null=True)
    cors_pack = models.CharField(max_length=5)

    def __str__(self):
        return self.cors_name