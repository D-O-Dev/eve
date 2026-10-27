from uuid import UUID

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

User = get_user_model()
router = Router(tags=["auth"])


class RegisterIn(Schema):
    email: str
    password: str
    full_name: str = ""


class LoginIn(Schema):
    email: str
    password: str


class UserOut(Schema):
    id: UUID
    email: str
    full_name: str
    locale: str


@router.post("/register", response={201: UserOut})
def register(request, data: RegisterIn):
    email = data.email.strip().lower()
    try:
        validate_email(email)
        validate_password(data.password)
    except ValidationError as e:
        raise HttpError(422, " ".join(e.messages))
    try:
        user = User.objects.create_user(email, data.password, full_name=data.full_name.strip())
    except IntegrityError:
        raise HttpError(409, "Un compte existe déjà avec cette adresse e-mail.")
    login(request, user)
    return 201, user


@router.post("/login", response=UserOut)
def login_view(request, data: LoginIn):
    user = authenticate(request, email=data.email.strip().lower(), password=data.password)
    if user is None:
        raise HttpError(401, "E-mail ou mot de passe incorrect.")
    login(request, user)
    return user


@router.post("/logout", auth=django_auth, response={204: None})
def logout_view(request):
    logout(request)
    return 204, None


@router.get("/me", auth=django_auth, response=UserOut)
def me(request):
    return request.user