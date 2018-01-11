from django.db import models
from course.models import Course

class Grade(models.Model):
    name = models.CharField(max_length=255)

class GradeCourse(models.Model):
    grade = models.ForeignKey(Grade, related_name='grade')
    course = models.ForeignKey(Course, related_name='course')

class GradeTeacher(models.Model):
    grade = models.ForeignKey(Grade, related_name='gradeteacher_grade')
    teacher = models.ForeignKey('auth.User', related_name='gradeteacher_teacher', on_delete=models.CASCADE)

class GradeStudent(models.Model):
    grade = models.ForeignKey(Grade, related_name='gradestudent_grade')
    student = models.ForeignKey('auth.User', related_name='gradestudent_student', on_delete=models.CASCADE)
