from django.db import models
from django.utils.text import slugify


# Create your models here.

class Types:
    PROGRAM_CHOICES = (
        (1, 'UnderGraduate'),
        (2, 'Graduate'),
        (3, 'Phd')
    )
    SEMESTER_CHOICES = (
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4rth'),
        (5, '5th'),
        (6, '6th'),
        (7, '7th'),
        (8, '8th'))


class Institute(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Institute, self).save(*args, **kwargs)


class Campus(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Campus, self).save(*args, **kwargs)


class Program(models.Model):
    category = models.IntegerField(default=1, choices=Types.PROGRAM_CHOICES)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Program, self).save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)


class Semester(models.Model):
    number = models.IntegerField(default=0, choices=Types.SEMESTER_CHOICES)


class Course(models.Model):
    name = models.CharField(max_length=200)
    credit_hour = models.FloatField()
    code = models.CharField(max_length=10)
    detail = models.CharField(max_length=300)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
