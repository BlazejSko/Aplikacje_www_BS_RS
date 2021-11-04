from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
    date_of_birth = models.DateField()
    user_type = models.CharField(max_length=45)


class Gym(models.Model):
    address: models.CharField(max_length=45)
    phone_number = models.CharField(max_length=9)
    email_address = models.CharField(max_length=45)


class Classrooms(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)


class Classes(models.Model):
    trainer = models.ForeignKey(Users, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField()


class UserClasses(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
