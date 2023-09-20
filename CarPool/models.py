from django.db import models

# Create your models here.

class Passenger(models.Model):
    pID = models.AutoField(primary_key=True)
    pName = models.TextField(max_length=128)
    pPhone = models.CharField(max_length=11)
    studentID = models.CharField(max_length=11)
    pPass = models.CharField(max_length=16)

class Vehicle(models.Model):
    vID = models.AutoField(primary_key=True)
    CarModel = models.TextField(max_length=128)
    CarType = models.TextField(max_length=128)
    capacity = models.IntegerField()
    brand = models.TextField(max_length=128)

class Driver(models.Model):
    dID = models.AutoField(primary_key=True)
    studentID = models.CharField(max_length=11)
    dName = models.TextField(max_length=128)
    dPhone = models.CharField(max_length=11)
    plate = models.CharField(max_length=7)
    carcolor = models.TextField(max_length=128)
    vID = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    dPass = models.CharField(max_length=16)

class Routes(models.Model):
    rID = models.AutoField(primary_key=True)
    rTo = models.TextField(max_length=128)
    rFrom = models.TextField(max_length=128)
    rPrice = models.IntegerField()

class RideRequest(models.Model):
    pID = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    dID  = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, default="")
    vID = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, default="")
    rID = models.ForeignKey(Routes, on_delete=models.CASCADE)
    passengers = models.IntegerField()
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()
    status = models.CharField(max_length=128, default="Pending")
    payment = models.CharField(max_length=128, default="Cash",)
