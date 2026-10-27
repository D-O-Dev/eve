from ninja import NinjaAPI

api = NinjaAPI(title="EVE API", version="1")
api.add_router("/auth", "identity.api.router")
api.add_router("/sectors", "sectors.api.router")
api.add_router("/companies", "organizations.api.router")