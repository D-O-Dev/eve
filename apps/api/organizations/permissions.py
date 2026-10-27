from django.http import Http404
from ninja.errors import HttpError

from billing.services import enabled_modules

from .models import Membership

# Zones toujours accessibles, même sans module actif (pour pouvoir renouveler un abonnement).
CORE_AREAS = {"company", "members"}

_SELLER = {"sales.view", "sales.create"}
_MANAGER = _SELLER | {"sales.cancel", "products.manage", "expenses.manage", "reports.view"}
_OWNER = _MANAGER | {"company.manage", "members.manage"}

ROLE_PERMISSIONS = {
    Membership.Role.OWNER: _OWNER,
    Membership.Role.MANAGER: _MANAGER,
    Membership.Role.SELLER: _SELLER,
}


def _area(permission: str) -> str:
    return permission.split(".")[0]


def effective_permissions(membership) -> set[str]:
    modules = enabled_modules(membership.company)
    return {
        p for p in ROLE_PERMISSIONS[membership.role]
        if _area(p) in CORE_AREAS or _area(p) in modules
    }


def authorize(user, company_id, permission=None):
    """Point d’entrée unique : appartenance, forfait, puis rôle."""
    membership = (
        Membership.objects.select_related("company")
        .filter(user=user, company_id=company_id)
        .first()
    )
    if membership is None:
        raise Http404  # on ne révèle pas l’existence de l’entreprise
    if permission:
        if _area(permission) not in CORE_AREAS and _area(permission) not in enabled_modules(membership.company):
            raise HttpError(403, "Cette fonction n’est pas incluse dans votre forfait.")
        if permission not in ROLE_PERMISSIONS[membership.role]:
            raise HttpError(403, "Vous n’avez pas le droit d’effectuer cette action.")
    return membership