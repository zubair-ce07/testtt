from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=60)
    cnic = models.CharField(max_length=20)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    vehicle_no = models.CharField(max_length=15)
    address = models.TextField()


class Room(models.Model):
    room_no = models.PositiveIntegerField()
    min_rent = models.DecimalField(decimal_places=2, max_digits=15)
    max_rent = models.DecimalField(decimal_places=2, max_digits=15)
    capacity = models.PositiveSmallIntegerField()
    category = models.CharField(max_length=50)
    floor = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {str(self.room_no)}"


class Reservation(models.Model):
    rent = models.DecimalField(decimal_places=2, max_digits=15)
    checkin = models.DateField()
    checkout = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Employee(models.Model):
    name = models.CharField(max_length=60)
    cnic = models.CharField(max_length=20)
    designation = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    salary = models.DecimalField(decimal_places=2, max_digits=15)
