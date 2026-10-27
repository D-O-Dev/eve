from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

User = get_user_model()


class UserTests(TestCase):
    def test_email_normalise_et_mot_de_passe_hache(self):
        u = User.objects.create_user("Awa@Example.COM", "motdepasse-solide-123")
        self.assertEqual(u.email, "awa@example.com")
        self.assertNotEqual(u.password, "motdepasse-solide-123")
        self.assertTrue(u.password.startswith("argon2"))
        self.assertTrue(u.check_password("motdepasse-solide-123"))

    def test_email_unique_sans_tenir_compte_de_la_casse(self):
        User.objects.create_user("awa@example.com", "x")
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user("AWA@example.com", "x")

    def test_utilisateur_normal_nest_pas_admin(self):
        u = User.objects.create_user("a@b.com", "x")
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_superuser)

    def test_superutilisateur(self):
        u = User.objects.create_superuser("root@b.com", "x")
        self.assertTrue(u.is_staff and u.is_superuser)

    def test_email_obligatoire(self):
        with self.assertRaises(ValueError):
            User.objects.create_user("", "x")