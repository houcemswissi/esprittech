from rest_framework import serializers
from rdiapp.models import *
from django.apps import apps
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Role, SchoolClassLevel, Up, ResearchTeam

CustomUser = get_user_model()

class EnumField(serializers.Field):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        self.enum_values = [e.value for e in enum]
        super().__init__(**kwargs)

    def to_representation(self, obj):
        if obj in self.enum_values:
            return obj
        raise serializers.ValidationError(f'Invalid value {obj}, expected one of {self.enum_values}')

    def to_internal_value(self, data):
        try:
            return self.enum(data).value
        except ValueError:
            raise serializers.ValidationError(f'Invalid value {data}, expected one of {self.enum_values}')

# Usage in a serializer
class RoleSerializer(serializers.ModelSerializer):
    status = EnumField(enum=Role)

    class Meta:
        model = Role
        fields = ['TEACHER', 'STUDENT']  # Include other fields of your model

class RoleChoiceSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[(role.value, role.name) for role in Role])

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=[(tag.name, tag.value) for tag in Role])
    birth_date = serializers.DateField(required=False)

    # Fields for Student
    student_cv = serializers.FileField(required=False)
    student_linkedin = serializers.URLField(required=False)
    student_picture = serializers.ImageField(required=False)
    student_graduation_year = serializers.IntegerField(required=False)
    school_class_level = serializers.PrimaryKeyRelatedField(queryset=SchoolClassLevel.objects.all(), required=False)

    # Fields for Teacher
    teacher_picture = serializers.ImageField(required=False)
    up = serializers.PrimaryKeyRelatedField(queryset=Up.objects.all(), required=False)
    research_team = serializers.PrimaryKeyRelatedField(queryset=ResearchTeam.objects.all(), required=False)

    def validate(self, data):
        role = data.get('role')
        if role == Role.STUDENT.value:
            required_fields = ['student_cv', 'student_linkedin', 'student_picture', 'student_graduation_year', 'school_class_level']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} is required for student registration.")
        elif role == Role.TEACHER.value:
            required_fields = ['teacher_picture', 'up', 'research_team']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(f"{field} is required for teacher registration.")
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'role': role,
            'birth_date': validated_data.pop('birth_date', None)
        }
        
        user = CustomUser.objects.create_user(**user_data)

        if role == Role.STUDENT.value:
            Student.objects.create(
                user=user,
                student_cv=validated_data.pop('student_cv'),
                student_linkedin=validated_data.pop('student_linkedin'),
                student_picture=validated_data.pop('student_picture'),
                student_graduation_year=validated_data.pop('student_graduation_year'),
                school_class_level=validated_data.pop('school_class_level')
            )
        elif role == Role.TEACHER.value:
            Teacher.objects.create(
                user=user,
                teacher_picture=validated_data.pop('teacher_picture'),
                up=validated_data.pop('up'),
                research_team=validated_data.pop('research_team')
            )

        return user



"""class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role'],
            birth_date=validated_data.get('birth_date')
        )
        return user



class TeacherSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Teacher
        fields = ['__all__','projects']


class StudentSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Application.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Application
        fields = ['__all__','Applications']    





class UserRegisterSerializer(serializers.Serializer):
    user = CustomUserSerializer()
    teacher = TeacherSerializer(required=False)
    student = StudentSerializer(required=False)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        
        if user.role == Role.TEACHER.value:
            teacher_data = validated_data.pop('teacher', {})
            Teacher.objects.create(user=user, **teacher_data)
        
        elif user.role == Role.STUDENT.value:
            student_data = validated_data.pop('student', {})
            Student.objects.create(user=user, **student_data)
        
        return user """   


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('id', 'user', 'student_cv', 'student_linkedin', 'student_graduation_year', 'school_class_level')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = Role.STUDENT.value
        user = UserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
    
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'up', 'research_team', 'is_head_supervisor')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = Role.TEACHER.value
        user = UserSerializer().create(user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher
    




def generate_serializers():
    app_models = apps.get_app_config('rdiapp').get_models()
    serializers_dict = {}

    for model in app_models:
        if ({model.__name__} not in ("CustomUser","Teacher","Student")):
            serializer_name = f"{model.__name__}Serializer"
            serializer_class = type(serializer_name, (serializers.ModelSerializer,), {
                "Meta": type("Meta", (), {
                    "model": model,
                    "fields": "__all__"
                })
            })
            serializers_dict[serializer_name] = serializer_class

    return serializers_dict

# Generate the serializers
generated_serializers = generate_serializers()

# Add the generated serializers to the global namespace
globals().update(generated_serializers)

