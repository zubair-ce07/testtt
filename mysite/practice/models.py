from django.db import models


""" Non-default Primary key """


class Fruit(models.Model):
    fruit_name = models.CharField(max_length=50, primary_key=True)


""" Many-to-one relationships """


class Manufecturer(models.Model):
    name = models.CharField(max_length=70)


class Car(models.Model):
    manufecturer = models.ForeignKey(Manufecturer, on_delete=models.CASCADE)


""" Many-to-many relationships """


class Toppings(models.Model):
    name = models.CharField(max_length=70)


class Pizza(models.Model):
    toppings = models.ManyToManyField(Toppings, on_delete=models.CASCADE)


""" Many-to-many relationships with extra fields """


class Person(models.Model):
    name = models.CharField(max_length=70)


class Group(models.Model):
    name = models.CharField(max_length=70)
    members = models.ManyToManyField(Person, on_delete=models.CASCADE)


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=80)

    # over-riding the model.save method to do something else before calling
    # the real method
    def save(self, *aregs, **kwargs):
        print("Saving the Membership model")
        super().save(*aregs, **kwargs)
        return


""" One-to-one relationships """


class Geolocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # custom method to print a model object as a string
    def __str__(self):
        return str(self.longitude) + str(self.latitude)


class Country(models.Model):
    name = models.CharField(max_length=70)
    date_of_inception = models.DateField()
    geolocation = models.OneToOneField(Geolocation)

    # Custom method to add row-level functionality
    # Helpful in keeping the business logic in one place
    def country_status(self):
        import datetime
        if datetime.date.today() - self.date_of_inception <= 18000:
            return "New country"
        else:
            return "Old Country"


""" Abstract inheritance """


class CommonInfo(models.Model):
    name = models.CharField(max_length=70)
    age = models.PositiveIntegerField()

    # This model need not have a table of its own
    class Meta:
        abstract = True


class Student(CommonInfo):
    section = models.CharField(max_length=75)
    # Table for this model will have three fields
    # name, age and section


class Teacher(CommonInfo):
    subject = models.CharField(max_length=75)
    # Table for this model will have three fields
    # name, age and subject
