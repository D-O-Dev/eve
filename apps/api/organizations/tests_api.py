from django.test import Client, TestCase

from organizations.models import Company

PWD = "Mot-de-passe-solide-2026!"


def post(client, url, data):
    return client.post(url, data=data, content_type="application/json")


def register(client, email="awa@example.com"):
    return post(client, "/api/auth/register", {"email": email, "password": PWD, "full_name": "Awa"})


class AuthApiTests(TestCase):
    def test_inscription_puis_me(self):
        c = Client()
        r = register(c)
        self.assertEqual(r.status_code, 201)
        me = c.get("/api/auth/me")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["email"], "awa@example.com")

    def test_me_sans_connexion(self):
        self.assertEqual(Client().get("/api/auth/me").status_code, 401)

    def test_mot_de_passe_faible_refuse(self):
        r = post(Client(), "/api/auth/register", {"email": "a@b.com", "password": "12345678"})
        self.assertEqual(r.status_code, 422)

    def test_email_deja_utilise_meme_en_majuscules(self):
        register(Client())
        r = register(Client(), "AWA@Example.com")
        self.assertEqual(r.status_code, 409)

    def test_connexion(self):
        register(Client())
        bad = post(Client(), "/api/auth/login", {"email": "awa@example.com", "password": "faux"})
        self.assertEqual(bad.status_code, 401)
        ok = post(Client(), "/api/auth/login", {"email": "AWA@example.com", "password": PWD})
        self.assertEqual(ok.status_code, 200)

    def test_deconnexion(self):
        c = Client()
        register(c)
        self.assertEqual(c.post("/api/auth/logout").status_code, 204)
        self.assertEqual(c.get("/api/auth/me").status_code, 401)


class CompanyApiTests(TestCase):
    def setUp(self):
        self.a, self.b = Client(), Client()
        register(self.a, "a@example.com")
        register(self.b, "b@example.com")

    def test_secteurs(self):
        r = self.a.get("/api/sectors")
        statuts = {s["code"]: s["status"] for s in r.json()}
        self.assertEqual(statuts["commerce"], "available")
        self.assertEqual(statuts["restauration"], "coming_soon")

    def test_creation_commerce(self):
        r = post(self.a, "/api/companies", {"name": "Boutique Awa", "sector_code": "commerce"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["role"], "owner")
        self.assertEqual(r.json()["currency_code"], "XOF")

    def test_secteur_bientot_disponible_refuse_par_le_serveur(self):
        r = post(self.a, "/api/companies", {"name": "Chez Maman", "sector_code": "restauration"})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Company.objects.count(), 0)

    def test_creation_sans_connexion(self):
        r = post(Client(), "/api/companies", {"name": "X", "sector_code": "commerce"})
        self.assertEqual(r.status_code, 401)

    def test_isolation_entre_entreprises(self):
        r = post(self.a, "/api/companies", {"name": "Boutique A", "sector_code": "commerce"})
        company_id = r.json()["id"]
        # Le propriétaire voit son entreprise.
        self.assertEqual(self.a.get(f"/api/companies/{company_id}").status_code, 200)
        # Un autre utilisateur, même avec le bon identifiant, ne la voit pas.
        self.assertEqual(self.b.get(f"/api/companies/{company_id}").status_code, 404)
        self.assertEqual(self.b.get("/api/companies").json(), [])