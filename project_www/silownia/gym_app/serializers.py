from rest_framework import serializers
from .models import UserProfile, Gym, Classrooms, Classes, UserClasses
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['url', 'phone_number', 'date_of_birth', 'user_type', 'user']


class GymSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gym
        fields = ['url', 'id', 'address', 'phone_number', 'email_address']


class ClassroomsSerializer(serializers.HyperlinkedModelSerializer):
    gym = serializers.SlugRelatedField(queryset=Gym.objects.all(), slug_field='address')

    class Meta:
        model = Classrooms
        fields = ['url', 'id', 'name', 'gym']


class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    trainer = serializers.SlugRelatedField(queryset=UserProfile.objects.all(), slug_field='full_name')
    classroom = serializers.SlugRelatedField(queryset=Classrooms.objects.all(), slug_field='name')
    participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='userclasses-detail')

    class Meta:
        model = Classes
        fields = ['url', 'trainer', 'id', 'classroom', 'start_date', 'end_date', 'max_capacity', 'current_capacity',
                  'participants']

        def validate_current_capacity(self, value):
            data = self.get_initial()
            if value < 0 or value > data.max_capacity:
                raise serializers.ValidationError("Don't make current capacity lower or equal to zero or greater to "
                                                  "max capacity", )
            return value

        def validate_max_capacity(self, value):
            if value <= 0:
                raise serializers.ValidationError("Don't make capacity lower or equal to zero", )
            return value


class UserClassesSerializer(serializers.HyperlinkedModelSerializer):
    class_id = serializers.SlugRelatedField(queryset=Classes.objects.all(), slug_field='id')
    user = serializers.SlugRelatedField(queryset=UserProfile.objects.all(), slug_field='id')

    class Meta:
        model = UserClasses
        fields = ['url', 'id', 'class_id', 'user']
