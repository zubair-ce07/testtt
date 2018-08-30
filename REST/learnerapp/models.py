from django.contrib.auth.models import AbstractUser
from django.db import models

STATUS_CHOICES = (('active', 'Active'),
                  ('archived', 'Archived'),
                  ('inprogress', 'In Progress'),)

LEVEL_CHOICES = (('beginner', 'Beginner'),
                 ('intermediate', 'Intermediate'),
                 ('advance', 'Advance'))


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = ((1, 'student'), (2, 'teacher'),)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)


class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    institute = models.CharField(max_length=100, blank=False)
    designation = models.CharField(max_length=50, default='Assistant Professor')

    def __str__(self):
        return self.user.__str__()

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField('Date of Birth', )
    university = models.CharField('University/Organization Name', max_length=100)

    def __str__(self):
        return self.user.__str__()

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=20)

    # instructors = models.ManyToManyField(Instructor)
    # students = models.ManyToManyField(Student, through=Enrollment)
#
#
# # class Enrollment(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     date_joined = models.DateField(default=datetime.date.today())
#     grade = models.CharField(max_length=1)