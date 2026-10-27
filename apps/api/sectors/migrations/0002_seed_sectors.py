from django.db import migrations

SECTORS = [
    ("commerce", "Commerce et boutiques", "Retail and shops", "available", 10),
    ("restauration", "Restauration et activités alimentaires", "Food and restaurants", "coming_soon", 20),
    ("services", "Services et prestations", "Services", "coming_soon", 30),
    ("transport", "Transport et livraison", "Transport and delivery", "coming_soon", 40),
    ("numerique", "Entreprises numériques", "Digital businesses", "coming_soon", 50),
]


def seed(apps, schema_editor):
    Sector = apps.get_model("sectors", "Sector")
    for code, fr, en, status, order in SECTORS:
        Sector.objects.update_or_create(
            code=code,
            defaults={"name_fr": fr, "name_en": en, "status": status, "sort_order": order},
        )


class Migration(migrations.Migration):
    dependencies = [("sectors", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]