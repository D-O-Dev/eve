import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    sector = models.ForeignKey("sectors.Sector", on_delete=models.PROTECT, related_name="companies")
    country = models.CharField(max_length=2, default="CI")
    currency_code = models.CharField(max_length=3, default="XOF")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Establishment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="establishments")
    name = models.CharField(max_length=150)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company"],
                condition=Q(is_default=True),
                name="one_default_establishment_per_company",
            )
        ]

    def __str__(self):
        return f"{self.company} · {self.name}"


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Propriétaire"
        MANAGER = "manager", "Gérant"
        SELLER = "seller", "Vendeur"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices)
    establishment = models.ForeignKey(
        Establishment, null=True, blank=True, on_delete=models.PROTECT, related_name="memberships"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "company"], name="one_membership_per_user_company"),
        ]