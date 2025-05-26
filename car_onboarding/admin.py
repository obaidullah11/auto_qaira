from django.contrib import admin
from .models import CarListing, CarImage

@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'model', 'year', 'location', 'price_per_day']

admin.site.register(CarImage)
