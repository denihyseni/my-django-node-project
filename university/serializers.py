from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()
        return user


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Faculty
        fields = ('id', 'name')


class AdministratorSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = models.Administrator
        fields = ('id', 'user', 'faculty', 'office')


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = models.Professor
        fields = ('id', 'user', 'faculty', 'title')


class StudentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = models.Student
        fields = ('id', 'user', 'faculty', 'enrollment_number')


class SubjectSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    students = StudentSerializer(read_only=True, many=True)
    professor_id = serializers.PrimaryKeyRelatedField(queryset=models.Professor.objects.all(), write_only=True, required=False)
    student_ids = serializers.PrimaryKeyRelatedField(queryset=models.Student.objects.all(), write_only=True, many=True, required=False)

    class Meta:
        model = models.Subject
        fields = ('id', 'name', 'faculty', 'professor', 'students', 'description', 'professor_id', 'student_ids')

    def create(self, validated_data):
        professor = validated_data.pop('professor_id', None)
        students = validated_data.pop('student_ids', [])
        subj = models.Subject.objects.create(**validated_data)
        if professor:
            subj.professor = professor
            subj.save()
        if students:
            subj.students.set(students)
        return subj

    def update(self, instance, validated_data):
        professor = validated_data.pop('professor_id', None)
        students = validated_data.pop('student_ids', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if professor is not None:
            instance.professor = professor
        if students is not None:
            instance.students.set(students)
        instance.save()
        return instance


class AdministratorCreateUpdateSerializer(AdministratorSerializer):
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer().create(user_data)
        admin = models.Administrator.objects.create(user=user, **validated_data)
        return admin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        return super().update(instance, validated_data)


class ProfessorCreateUpdateSerializer(ProfessorSerializer):
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer().create(user_data)
        prof = models.Professor.objects.create(user=user, **validated_data)
        return prof

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        return super().update(instance, validated_data)


class StudentCreateUpdateSerializer(StudentSerializer):
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer().create(user_data)
        stu = models.Student.objects.create(user=user, **validated_data)
        return stu

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        return super().update(instance, validated_data)

class EnrollmentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    professor_name = serializers.CharField(source='subject.professor.user.first_name', read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ('id', 'student', 'student_username', 'subject', 'subject_name', 'professor_name', 'enrolled_date', 'grade', 'score')


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    """Detailed enrollment with full nested objects."""
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ('id', 'student', 'subject', 'enrolled_date', 'grade', 'score')