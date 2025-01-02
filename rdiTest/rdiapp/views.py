from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RoleForm
from rest_framework import generics , permissions , viewsets
from rdiapp.permissions import IsOwnerOrReadOnly
from rdiapp.models import *
from rdiapp.enums import *
from rest_framework.decorators import api_view
from rdiapp.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model , authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

User = get_user_model()


def index(request):
    return HttpResponse("You're looking to the index page.")

"""

def index(request):
    return render(request, 'index.html') 
"""



def choose_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            # Process the form data
            role = form.cleaned_data['role']
            # Redirect or render a success page
            return redirect('success_url')  # Replace 'success_url' with your actual success URL
    else:
        form = RoleForm()
    
    return render(request, 'choose_role.html', {'form': form})



"""class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

"""
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully",
        }, status=status.HTTP_201_CREATED)
        """
class RegisterStudentView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterStudentView(generics.CreateAPIView):
    
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]
    """def post(self, request, *args, **kwargs):
                student_serializer = generated_serializers["StudentSerializer"](data={'user': User.id, 'student_id': request.data.get('student_id'), 'role': 'student'})
                if student_serializer.is_valid():
                    student_serializer.save()
                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


class RegisterTeacherView(generics.CreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.AllowAny]

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    """def post(self, request, *args, **kwargs):
        user_serializer = generated_serializers["UserSerializer"](data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            role = request.data.get('role')
            if role == 'student':
                return RegisterStudentView(User)
                student_serializer = generated_serializers["StudentSerializer"](data={'user': user.id, 'student_id': request.data.get('student_id'), 'role': 'student'})
                if student_serializer.is_valid():
                    student_serializer.save()
                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif role == 'teacher':
                return RegisterStudentView(User)
                teacher_serializer = generated_serializers["TeacherSerializer"](data={'user': user.id, 'teacher_id': request.data.get('teacher_id'), 'role': 'teacher'})
                if teacher_serializer.is_valid():
                    teacher_serializer.save()
                else:
                    return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
    




class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ViewSet for the User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = generated_serializers["UserSerializer"]

# ViewSet for the Teacher model
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = generated_serializers["TeacherSerializer"]

# ViewSet for the Student model
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = generated_serializers["StudentSerializer"]

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class ProjectList(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = generated_serializers["ProjectSerializer"]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

class ProjectCreate(generics.CreateAPIView):  
    queryset = Project.objects.all()
    serializer_class = generated_serializers["ProjectSerializer"]

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = generated_serializers["ProjectSerializer"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class ResearchTeamDetail(generics.RetrieveAPIView):
    queryset = ResearchTeam.objects.all()
    serializer_class = generated_serializers["ResearchTeamSerializer"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ApplicationList(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = generated_serializers["ApplicationSerializer"]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

class ApplicationCreate(generics.CreateAPIView):  
    queryset = Application.objects.all()
    serializer_class = generated_serializers["ApplicationSerializer"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RoleChoiceView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RoleChoiceSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data['role']
            if role == Role.TEACHER.value:
                return redirect('teacher-create')
            elif role == Role.STUDENT.value:
                return redirect('student-create')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""class TeacherCreate(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = generated_serializers["TeacherSerializer"]  
"""

class TeacherCreate(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = generated_serializers["TeacherSerializer"]   

class StudentCreate(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = generated_serializers["StudentSerializer"]     



    
    

    
