from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
    date_of_birth = models.DateField()
    user_type = models.CharField(max_length=45)

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.full_name


class Gym(models.Model):
    address = models.CharField(max_length=45, default='test')
    phone_number = models.CharField(max_length=9, unique=True)
    email_address = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.address


class Classrooms(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name


class Classes(models.Model):
    trainer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='trainer')
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_capacity = models.IntegerField()
    current_capacity = models.IntegerField()

    def __str__(self):
        return str(self.start_date)


class UserClasses(models.Model):
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_id

