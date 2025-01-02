"""
URL configuration for rdiTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import *
from rdiapp.views import *
from django.contrib import admin

router = DefaultRouter()
router.register(r'users', UserViewSet ,  basename='user')
router.register(r'teachers', TeacherViewSet ,  basename='teacher')
router.register(r'students', StudentViewSet ,  basename='student')


"""urlpatterns = [
    path("", index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('student/signup/', StudentCreate.as_view(), name='StudentSignup'),
    path('teacher/add-project/', ProjectCreate.as_view(), name='Add Project'),
    path('projects/', ProjectList.as_view(), name='Projects'),
    path('apply-project/', ApplicationCreate.as_view(), name='Application'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='Project Details'),
    path('login/', LoginView.as_view(), name="login"),
    path('choose-role/', RoleChoiceView.as_view(), name='role-choice'),
    path('user-register/', UserRegisterView.as_view(), name='user-register'),
    path('', include(router.urls)),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]"""

urlpatterns = [
    path('', include(router.urls)),
    #path('register/', UserRegisterView.as_view(), name='user-register'),
    path('register/student/', RegisterStudentView.as_view(), name='register_student'),
    path('register/teacher/', RegisterTeacherView.as_view(), name='register_teacher'),
    path('login/', LoginView.as_view(), name='login'),
]