from django.db import transaction

from sectors.models import Sector

from .models import Company, Establishment, Membership

from billing.models import Plan, Subscription


class SectorNotAvailable(Exception):
    """Le secteur existe, mais n’est pas encore ouvert à la sélection."""


@transaction.atomic
def create_company(*, user, name, sector_code):
    name = name.strip()
    if not name:
        raise ValueError("Le nom de l’entreprise est obligatoire.")
    sector = Sector.objects.get(code=sector_code)
    # Premium sera géré avec les forfaits (phase 5) : pour l’instant, seul « disponible » passe.
    if sector.status != Sector.Status.AVAILABLE:
        raise SectorNotAvailable(sector_code)
    company = Company.objects.create(name=name, sector=sector)
    Establishment.objects.create(company=company, name="Principal", is_default=True)
    Membership.objects.create(user=user, company=company, role=Membership.Role.OWNER)
    Subscription.objects.create(company=company, plan=Plan.objects.get(code="free"))
    return company