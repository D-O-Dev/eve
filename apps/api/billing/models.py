from django.db import models
from django.utils import timezone


class Plan(models.Model):
    code = models.SlugField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlanModule(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="modules")
    module_code = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["plan", "module_code"], name="one_module_per_plan"),
        ]


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Actif"
        GRACE = "grace", "Période de grâce"
        EXPIRED = "expired", "Expiré"

    company = models.OneToOneField("organizations.Company", on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    current_period_end = models.DateTimeField(null=True, blank=True)
    grace_until = models.DateTimeField(null=True, blank=True)

    def is_in_effect(self) -> bool:
        if self.status == self.Status.ACTIVE:
            return True
        if self.status == self.Status.GRACE:
            return self.grace_until is not None and timezone.now() < self.grace_until
        return False