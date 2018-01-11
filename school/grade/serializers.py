from rest_framework import serializers
from grade.models import Grade,GradeCourse, GradeTeacher, GradeStudent
from course.serializers import CourseSerializer
from user.serializers import UserDetailSerializer

# Grade Course
class GradeCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GradeCourse
        fields = ('id', 'grade', 'course', )

class GradeCourseDetailSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = GradeCourse
        fields = ('course_detail', )


# Grade Teachers
class GradeTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeTeacher
        fields = ('id', 'grade', 'teacher', )

class GradeTeacherDetailSerializer(serializers.ModelSerializer):
    teacher_detail = UserDetailSerializer(source='teacher', read_only=True)
    class Meta:
        model = GradeTeacher
        fields = ('teacher_detail', )


# Grade Student
class GradeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeStudent
        fields = ('id', 'grade', 'student', )

class GradeStudentDetailSerializer(serializers.ModelSerializer):
    student_detail = UserDetailSerializer(source='student', read_only=True)
    class Meta:
        model = GradeStudent
        fields = ('student_detail', )



# Grade
class GradeSerializer(serializers.ModelSerializer):
    courses = GradeCourseDetailSerializer(source='grade', many=True, read_only=True)
    students = GradeStudentDetailSerializer(source='gradestudent_grade', many=True, read_only=True)
    teachers = GradeTeacherDetailSerializer(source='gradeteacher_grade', many=True, read_only=True)
    
    class Meta:
        model = Grade
        fields = ('id', 'name', 'courses', 'students', 'teachers', )

