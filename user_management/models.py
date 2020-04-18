from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    image = models.TextField()

    class Meta:
        db_table = 'users'
