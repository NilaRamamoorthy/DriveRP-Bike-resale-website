# Base
from django.db import models

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos/')
    name = models.CharField(max_length=100, default='DriveRP')
    footer_bike = models.ImageField(upload_to='footer_bikes/', blank=True, null=True)
    footer_logo = models.ImageField(upload_to='footer_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# Login Page


class LoginImage(models.Model):
    image = models.ImageField(upload_to='login/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.alt_text or "Login Image"



# Home

class HomeContent(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=100, default="Buy Now")
    button_link = models.URLField(default="buy_bike")

    def __str__(self):
        return self.title

class BikeCarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or f"Bike Image {self.id}"


class RiderSection(models.Model):
    image = models.ImageField(upload_to='rider/')
    content = models.TextField()
    button_text = models.CharField(max_length=100, default="Read More")
    button_link = models.CharField(max_length=255, default="about_us") 

    def __str__(self):
        return "Rider Section"
    


class SupportFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='support_features/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title





class CustomerReview(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_or_default(self):
        if self.image:
            return self.image.url
        return '/static/images/default_user.png'  # Make sure this default image exists




class TrustedRidersSection(models.Model):
    heading = models.CharField(max_length=200, default="Trusted by Riders Like You")
    description = models.TextField(default="From smooth sales to great secondhand finds...")
    image = models.ImageField(upload_to='trusted_riders/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.heading




class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question



class AboutSection(models.Model):
    about_image = models.ImageField(upload_to='about/', help_text="Image for the About Us section (left side)")
    mission_image = models.ImageField(upload_to='about/', help_text="Image for the Mission section background")

    def __str__(self):
        return "About Page Content"

class ApproachSectionImage(models.Model):
    image = models.ImageField(upload_to='approach/')
    order = models.PositiveIntegerField(default=0, help_text="Controls image order (0 = top left)")

    def __str__(self):
        return f"Image {self.order}"
