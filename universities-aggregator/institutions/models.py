from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Institution(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Institution, self).save(*args, **kwargs)


class Campus(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    institute = models.ForeignKey(Institution, related_name='institute_campuses', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'institute')

    def __str__(self):
        return f'{self.name} / {self.institute.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Campus, self).save(*args, **kwargs)


class Program(models.Model):
    CATEGORY_CHOICES = (
        (1, 'UnderGraduate'),
        (2, 'Graduate'),
        (3, 'Phd')
    )
    category = models.IntegerField(default=1, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    campus = models.ForeignKey(Campus, related_name='campus_programs', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'campus')

    def __str__(self):
        return f'{self.name} / {self.campus.institute.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Program, self).save(*args, **kwargs)


class Semester(models.Model):
    SEMESTER_CHOICES = (
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4rth'),
        (5, '5th'),
        (6, '6th'),
        (7, '7th'),
        (8, '8th'))
    number = models.IntegerField(default=0, choices=SEMESTER_CHOICES)
    program = models.ForeignKey(Program, default='', related_name='program_semesters', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('number', 'program')

    def __str__(self):
        return f'{self.number} | {self.program.name} | {self.program.campus} '


class Course(models.Model):
    name = models.CharField(max_length=200)
    credit_hour = models.FloatField()
    code = models.CharField(max_length=10)
    semester = models.ForeignKey(Semester, related_name='semester_courses', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name='program_courses', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'program')
