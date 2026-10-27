from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

from sectors.models import Sector

from .models import Membership
from .services import SectorNotAvailable, create_company

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
    membership = get_object_or_404(
        Membership.objects.select_related("company"),
        user=request.user,
        company_id=company_id,
    )
    return _out(membership)