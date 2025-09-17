from django.db import models

class ContactSubmission(models.Model):
    REASONS = [
        ("General Enquiry", "General Enquiry"),
        ("Buy a Bike", "Buy a Bike"),
        ("Sell a Bike", "Sell a Bike"),
        ("Exchange a Bike", "Exchange a Bike"),
        ("RTO Service", "RTO Service"),
        ("Others", "Others"),
    ]

    SOURCES = [
        ("OLX", "OLX"),
        ("Instagram", "Instagram"),
        ("Youtube", "Youtube"),
        ("Google", "Google"),
        ("Website", "Website"),
        ("Facebook", "Facebook"),
        ("Walk-in", "Walk-in"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    reason = models.CharField(max_length=50, choices=REASONS)
    source = models.CharField(max_length=50, choices=SOURCES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.reason}"
