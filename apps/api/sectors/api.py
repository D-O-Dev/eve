from ninja import Router, Schema
from ninja.security import django_auth

from .models import Sector

router = Router(tags=["sectors"], auth=django_auth)


class SectorOut(Schema):
    code: str
    name_fr: str
    name_en: str
    status: str


@router.get("", response=list[SectorOut])
def list_sectors(request):
    return Sector.objects.all()