from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

from sectors.models import Sector

from .models import Membership
from .services import SectorNotAvailable, create_company

from billing.services import enabled_modules

from .permissions import authorize, effective_permissions

router = Router(tags=["companies"], auth=django_auth)


class CompanyIn(Schema):
    name: str
    sector_code: str


class CompanyOut(Schema):
    id: UUID
    name: str
    sector_code: str
    country: str
    currency_code: str
    role: str


def _out(m: Membership) -> dict:
    c = m.company
    return {
        "id": c.id,
        "name": c.name,
        "sector_code": c.sector_id,
        "country": c.country,
        "currency_code": c.currency_code,
        "role": m.role,
    }


@router.get("", response=list[CompanyOut])
def list_companies(request):
    memberships = Membership.objects.filter(user=request.user).select_related("company")
    return [_out(m) for m in memberships]


@router.post("", response={201: CompanyOut})
def create(request, data: CompanyIn):
    try:
        company = create_company(user=request.user, name=data.name, sector_code=data.sector_code)
    except ValueError as e:
        raise HttpError(422, str(e))
    except Sector.DoesNotExist:
        raise HttpError(404, "Secteur inconnu.")
    except SectorNotAvailable:
        raise HttpError(403, "Ce secteur n’est pas encore disponible.")
    membership = Membership.objects.select_related("company").get(user=request.user, company=company)
    return 201, _out(membership)


@router.get("/{company_id}", response=CompanyOut)
def get_company(request, company_id: UUID):
    return _out(authorize(request.user, company_id))

class AccessOut(Schema):
    role: str
    subscription_status: str
    modules: list[str]
    permissions: list[str]


@router.get("/{company_id}/access", response=AccessOut)
def access(request, company_id: UUID):
    m = authorize(request.user, company_id)
    sub = getattr(m.company, "subscription", None)
    return {
        "role": m.role,
        "subscription_status": sub.status if sub else "none",
        "modules": sorted(enabled_modules(m.company)),
        "permissions": sorted(effective_permissions(m)),
    }