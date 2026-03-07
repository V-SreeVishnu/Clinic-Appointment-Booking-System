from django.db import models

class Appointment(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    token = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.date} - Token {self.token}"