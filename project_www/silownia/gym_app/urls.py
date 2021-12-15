from django.urls import path

from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('gyms', views.GymList.as_view(), name=views.GymList.name),
    path('gyms/<int:pk>', views.GymDetail.as_view(), name=views.GymDetail.name),
    path('classrooms', views.ClassroomList.as_view(), name=views.ClassroomList.name),
    path('classrooms/<int:pk>', views.ClassroomDetail.as_view(), name=views.ClassroomDetail.name),
    path('users', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('classes', views.ClassesList.as_view(), name=views.ClassesList.name),
    path('classes/<int:pk>', views.ClassesDetail.as_view(), name=views.ClassesDetail.name),
    path('userclasses', views.UserClassesList.as_view(), name=views.UserClassesList.name),
    path('userclasses/<int:pk>', views.UserClassesDetail.as_view(), name=views.UserClassesDetail.name),
    path('users/<int:user_id>/userclasses', views.UserClassesForGivenUserList.as_view(), name=views.UserClassesForGivenUserList.name),
    path('users/<int:user_id>/userclasses/<int:pk>', views.UserClassesForGivenUserDetail.as_view(), name=views.UserClassesForGivenUserDetail.name),
]