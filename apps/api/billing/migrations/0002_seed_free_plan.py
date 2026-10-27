from django.db import migrations

MODULES = ["sales", "products", "expenses", "reports"]


def seed(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    PlanModule = apps.get_model("billing", "PlanModule")
    plan, _ = Plan.objects.update_or_create(code="free", defaults={"name": "Gratuit"})
    for code in MODULES:
        PlanModule.objects.get_or_create(plan=plan, module_code=code)


class Migration(migrations.Migration):
    dependencies = [("billing", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]