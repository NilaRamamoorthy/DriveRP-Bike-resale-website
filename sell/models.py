from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Variant(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    launch_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class SellImage(models.Model):
    image = models.ImageField(upload_to='sell_images/')
    active = models.BooleanField(default=True)  # optional if you want to rotate/display latest

    def __str__(self):
        return f"Sell Image {self.id}"


class HowItWorksStep(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='how_it_works/')
    order = models.PositiveIntegerField(default=0)  # To keep them in the correct sequence

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"

from django.db import models

class SellHero(models.Model):
    heading = models.TextField()
    image = models.ImageField(upload_to='sell_hero/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.heading[:50]
