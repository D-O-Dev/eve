from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from sectors.models import Sector

from .models import Company, Establishment, Membership
from .services import SectorNotAvailable, create_company

User = get_user_model()


class CreateCompanyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("awa@example.com", "x")

    def test_creation_commerce(self):
        c = create_company(user=self.user, name="Boutique Awa", sector_code="commerce")
        self.assertEqual((c.country, c.currency_code), ("CI", "XOF"))
        self.assertTrue(c.establishments.get().is_default)
        m = Membership.objects.get(user=self.user, company=c)
        self.assertEqual(m.role, Membership.Role.OWNER)

    def test_secteur_bientot_disponible_refuse(self):
        with self.assertRaises(SectorNotAvailable):
            create_company(user=self.user, name="Chez Maman", sector_code="restauration")
        self.assertEqual(Company.objects.count(), 0)

    def test_secteur_inconnu(self):
        with self.assertRaises(Sector.DoesNotExist):
            create_company(user=self.user, name="X", sector_code="inexistant")

    def test_nom_vide_ne_cree_rien(self):
        with self.assertRaises(ValueError):
            create_company(user=self.user, name="   ", sector_code="commerce")
        self.assertEqual(Company.objects.count(), 0)

    def test_un_utilisateur_plusieurs_entreprises(self):
        create_company(user=self.user, name="Boutique A", sector_code="commerce")
        create_company(user=self.user, name="Boutique B", sector_code="commerce")
        self.assertEqual(Membership.objects.filter(user=self.user).count(), 2)

    def test_un_seul_etablissement_par_defaut(self):
        c = create_company(user=self.user, name="Boutique A", sector_code="commerce")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Establishment.objects.create(company=c, name="Autre", is_default=True)

    def test_pas_de_doublon_appartenance(self):
        c = create_company(user=self.user, name="Boutique A", sector_code="commerce")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Membership.objects.create(user=self.user, company=c, role=Membership.Role.MANAGER)

    def test_secteurs_initiaux(self):
        statuts = dict(Sector.objects.values_list("code", "status"))
        self.assertEqual(statuts["commerce"], "available")
        for code in ("restauration", "services", "transport", "numerique"):
            self.assertEqual(statuts[code], "coming_soon")