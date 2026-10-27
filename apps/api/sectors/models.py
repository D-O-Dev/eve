from django.db import models


class Sector(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Disponible"
        COMING_SOON = "coming_soon", "Bientôt disponible"
        PREMIUM = "premium", "Premium"

    code = models.SlugField(primary_key=True)
    name_fr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMING_SOON)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name_fr