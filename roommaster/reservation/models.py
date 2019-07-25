from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


categories = (
    ("General", "General"),
    ("Family", "Family"),
    ("Suite", "Suite")
)


class Customer(models.Model):
    name = models.CharField(max_length=60)
    cnic = models.CharField(max_length=20, unique=True, validators=[
            RegexValidator(
                regex='^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$',
                message='Use XXXXX-XXXXXXX-X format',
            )])
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    vehicle_no = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.cnic


class Room(models.Model):
    room_no = models.PositiveIntegerField()
    min_rent = models.DecimalField(decimal_places=2, max_digits=15)
    max_rent = models.DecimalField(decimal_places=2, max_digits=15)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    category = models.CharField(max_length=10, choices=categories, default="General")
    floor = models.PositiveIntegerField()

    def __str__(self):
        return str(self.room_no)


class Reservation(models.Model):
    rent = models.DecimalField(decimal_places=2, max_digits=15)
    checkin = models.DateField()
    checkout = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Employee(models.Model):
    name = models.CharField(max_length=60)
    cnic = models.CharField(max_length=20, unique=True, validators=[
            RegexValidator(
                regex='^[0-9+]{5}-[0-9+]{7}-[0-9]{1}$',
                message='Use XXXXX-XXXXXXX-X format',
            )])
    designation = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    salary = models.DecimalField(decimal_places=2, max_digits=15)
