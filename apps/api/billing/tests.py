from datetime import timedelta

from django.contrib.auth import get_user_model
from django.http import Http404
from django.test import Client, TestCase
from django.utils import timezone
from ninja.errors import HttpError

from organizations.models import Company, Membership
from organizations.permissions import authorize
from organizations.services import create_company

from .models import PlanModule, Subscription
from .services import enabled_modules

User = get_user_model()


class Base(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner@example.com", "x")
        self.seller = User.objects.create_user("seller@example.com", "x")
        self.outsider = User.objects.create_user("outsider@example.com", "x")
        self.company = create_company(user=self.owner, name="Boutique A", sector_code="commerce")
        Membership.objects.create(user=self.seller, company=self.company, role=Membership.Role.SELLER)

    def fresh(self):
        return Company.objects.get(pk=self.company.pk)


class EntitlementTests(Base):
    def test_forfait_gratuit_a_la_creation(self):
        self.assertEqual(enabled_modules(self.fresh()), {"sales", "products", "expenses", "reports"})

    def test_abonnement_expire_aucun_module(self):
        Subscription.objects.filter(company=self.company).update(status="expired")
        self.assertEqual(enabled_modules(self.fresh()), set())

    def test_periode_de_grace_en_cours(self):
        Subscription.objects.filter(company=self.company).update(
            status="grace", grace_until=timezone.now() + timedelta(days=3)
        )
        self.assertIn("sales", enabled_modules(self.fresh()))

    def test_periode_de_grace_terminee(self):
        Subscription.objects.filter(company=self.company).update(
            status="grace", grace_until=timezone.now() - timedelta(days=1)
        )
        self.assertEqual(enabled_modules(self.fresh()), set())


class AuthorizeTests(Base):
    def test_proprietaire_peut_annuler_une_vente(self):
        m = authorize(self.owner, self.company.id, "sales.cancel")
        self.assertEqual(m.role, "owner")

    def test_vendeur_ne_peut_pas_annuler(self):
        with self.assertRaises(HttpError) as ctx:
            authorize(self.seller, self.company.id, "sales.cancel")
        self.assertEqual(ctx.exception.status_code, 403)

    def test_etranger_voit_introuvable(self):
        with self.assertRaises(Http404):
            authorize(self.outsider, self.company.id, "sales.view")

    def test_module_hors_forfait_refuse(self):
        PlanModule.objects.filter(plan_id="free", module_code="sales").delete()
        with self.assertRaises(HttpError) as ctx:
            authorize(self.owner, self.company.id, "sales.view")
        self.assertEqual(ctx.exception.status_code, 403)

    def test_gestion_entreprise_possible_meme_expire(self):
        Subscription.objects.filter(company=self.company).update(status="expired")
        m = authorize(self.owner, self.company.id, "company.manage")
        self.assertEqual(m.role, "owner")


class AccessApiTests(Base):
    def _get(self, user):
        c = Client()
        c.force_login(user)
        return c.get(f"/api/companies/{self.company.id}/access")

    def test_acces_proprietaire(self):
        data = self._get(self.owner).json()
        self.assertEqual(data["role"], "owner")
        self.assertEqual(data["subscription_status"], "active")
        self.assertIn("sales.cancel", data["permissions"])

    def test_acces_vendeur(self):
        data = self._get(self.seller).json()
        self.assertIn("sales.create", data["permissions"])
        self.assertNotIn("sales.cancel", data["permissions"])