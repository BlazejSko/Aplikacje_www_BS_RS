from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Gym, Classrooms, Classes, UserProfile, UserClasses
from .serializers import GymSerializer, ClassroomsSerializer, UserProfileSerializer, ClassesSerializer, \
    UserClassesSerializer

from rest_framework import permissions
from django_filters import DateTimeFilter, FilterSet
from django.contrib.auth.models import User


class GymList(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    name = 'gym-list'
    search_fields = ['address', 'phone_number', 'email_address']
    ordering_fields = ['address', 'phone_number', 'email_address']
    # permission_classes = [permissions.IsAdminUser]


class GymDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    name = 'gym-detail'
    # permission_classes = [permissions.IsAdminUser]


class ClassroomList(generics.ListCreateAPIView):
    queryset = Classrooms.objects.all()
    serializer_class = ClassroomsSerializer
    name = 'classrooms-list'
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [permissions.IsAdminUser]


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classrooms.objects.all()
    serializer_class = ClassroomsSerializer
    name = 'classrooms-detail'
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = [permissions.IsAdminUser]


class UserFilter(FilterSet):
    from_birthdate = DateTimeFilter(field_name='date_of_birth', lookup_expr='gte')
    to_birthdate = DateTimeFilter(field_name='date_of_birth', lookup_expr='lte')

    class Meta:
        model = UserProfile
        fields = ['from_birthdate', 'to_birthdate', 'phone_number', 'user__first_name', 'user__last_name']


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'userprofile-list'
    filter_class = UserFilter
    search_fields = ['phone_number', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__last_name', 'date_of_birth']
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'userprofile-detail'
    permission_classes = [permissions.IsAdminUser]


class ClassesFilter(FilterSet):
    from_date = DateTimeFilter(field_name='start_date', lookup_expr='gte')
    to_date = DateTimeFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = Classes
        fields = ['from_date', 'to_date', 'classroom']


class TrainerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        print(request.user.id)
        user = UserProfile.objects.get(id=request.user.id)

        if user.user_type == 'trainer' or request.user.is_superuser == 1:
            return True
        else:
            return False


class ClassesList(generics.ListCreateAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    name = 'classes-list'
    filter_class = ClassesFilter
    search_fields = ['trainer__user__first_name', 'trainer__user__last_name']
    ordering_fields = ['trainer', 'classroom']
    permission_classes = (TrainerPermission | permissions.IsAdminUser,)


class ClassesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    name = 'classes-detail'
    permission_classes = (TrainerPermission | permissions.IsAdminUser,)


class UserClassesList(generics.ListCreateAPIView):
    queryset = UserClasses.objects.all()
    serializer_class = UserClassesSerializer
    name = 'userclasses-list'


class UserClassesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserClasses.objects.all()
    serializer_class = UserClassesSerializer
    name = 'userclasses-detail'


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = Options. Head, Get
        print(obj.user_id, request.user.id)
        return obj.user_id == request.user.id


class UserClassesForGivenUserList(generics.ListCreateAPIView):
    serializer_class = UserClassesSerializer
    name = 'userclassesforgivenuser-list'

    def get_queryset(self):
        return UserClasses.objects.filter(user_id=self.kwargs['user_id'])
    permission_classes = (IsCurrentUser | permissions.IsAdminUser,)
    #permission_classes = (IsCurrentUser)


class UserClassesForGivenUserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserClassesSerializer
    name = 'userclassesforgivenuser-detail'

    def get_queryset(self):
        return UserClasses.objects.filter(user_id=self.kwargs['user_id'])
    permission_classes = (IsCurrentUser | permissions.IsAdminUser,)
    #permission_classes = (IsCurrentUser)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'gyms': reverse(GymList.name, request=request),
                         'classrooms': reverse(ClassroomList.name, request=request),
                         'users': reverse(UserList.name, request=request),
                         'classes': reverse(ClassesList.name, request=request),
                         'userclasses': reverse(UserClassesList.name, request=request),
                         })
