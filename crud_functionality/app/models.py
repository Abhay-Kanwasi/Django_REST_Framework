from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    roll_no = models.IntegerField(unique=True)
    city = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name