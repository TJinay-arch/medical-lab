from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    doctors = models.ManyToManyField("core.Doctor", related_name="services", blank=True)

    def __str__(self):
        return self.name
