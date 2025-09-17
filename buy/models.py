from django.db import models
from sell.models import Brand, Model, Variant
class BikeListing(models.Model):
    
    CATEGORY_CHOICES = [
        ('scooty', 'Scooty'),
        ('motorbike', 'Motor Bike'),
        ('ev', 'EV'),
    ]
    TRANSMISSION_CHOICES = [
    ('Manual', 'Manual'),
    ('Auto', 'Auto'),
    ('Unknown', 'Unknown'),
]
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    variant = models.CharField(max_length=100)
    year = models.IntegerField()
    engine_cc = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    kilometers_driven = models.IntegerField()
    owner = models.CharField(max_length=20)  # e.g., '1st Owner'
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='buy_bikes/', null=True, blank=True)
    booked = models.BooleanField(default=False)
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    refurbished = models.BooleanField(default=False)
    rto_state = models.CharField(max_length=100, null=True, blank=True, default='Unknown')
    rto_city = models.CharField(max_length=100, null=True, blank=True, default='Unknown')


    registration_year = models.PositiveIntegerField(null=True, blank=True)
    rc_available = models.BooleanField(default=False)
    finance = models.BooleanField(default=False)
    insurance = models.BooleanField(default=False)
    warranty = models.BooleanField(default=False)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='Unknown')

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='motorbike')



    ignition_type = models.CharField(max_length=100, default='Kick & Self Start')
    front_brake_type = models.CharField(max_length=50, default='Drum')
    rear_brake_type = models.CharField(max_length=50, default='Drum')
    abs = models.BooleanField(default=False)
    odometer_type = models.CharField(max_length=50, default='Analogue')
    wheel_type = models.CharField(max_length=50, default='Steel')

    
    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"



# models.py
class BikeImage(models.Model):
    bike = models.ForeignKey(BikeListing, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='bike_gallery/')




class BookingStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='booking_steps/')

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"