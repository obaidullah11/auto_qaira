from django.db import models
# from django.contrib.auth import get_user_model
from users.models import User  
# Assuming you have a custom user model in users app
# User = get_user_model()
# models.py


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CarListing(models.Model):
    TRANSMISSION_CHOICES = [('Automatic', 'Automatic'), ('Manual', 'Manual')]
    FUEL_CHOICES = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Hybrid', 'Hybrid'), ('Electric', 'Electric')]
    AVAILABILITY_CHOICES = [('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')]
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'), ('Truck', 'Truck'), ('Van', 'Van')
    ]
    FUEL_POLICY_CHOICES = [('Full_to_Full', 'Full to Full'), ('Prepaid', 'Prepaid')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Car details
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    engine_capacity = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=20, unique=True)
    mileage = models.PositiveIntegerField()
    seating_capacity = models.PositiveSmallIntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)

    # Location
    location = models.CharField(max_length=255)
   
    pickup_location = models.CharField(max_length=255)

    # Availability
    available_from = models.DateField()
    available_until = models.DateField()
    availability_type = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES)
    delivery_available = models.BooleanField(default=False)

    # Pricing
    price_per_day = models.PositiveIntegerField()
    price_per_week = models.PositiveIntegerField()
    price_per_month = models.PositiveIntegerField()
    security_deposit = models.PositiveIntegerField()
    minimum_rent_days = models.PositiveIntegerField()

    
 

    # Features
    air_conditioning = models.BooleanField(default=True)
    gps = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    usb_charging = models.BooleanField(default=False)
    child_seat = models.BooleanField(default=False)
    fuel_policy = models.CharField(max_length=20, choices=FUEL_POLICY_CHOICES)
    additional_notes = models.TextField(blank=True, null=True)

    # Driver
    driver_allowed = models.BooleanField(default=True)
    with_driver_only = models.BooleanField(default=False)
    driver_charges_per_day = models.PositiveIntegerField(default=0)
    max_km_per_day = models.PositiveIntegerField()
    extra_km_charge = models.PositiveIntegerField()
    cancellation_policy = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    images = models.JSONField(default=list, blank=True, null=True, help_text="Store list of image URLs or metadata as JSON")

    def __str__(self):
        return self.title


class CarImage(models.Model):
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car.title}"
