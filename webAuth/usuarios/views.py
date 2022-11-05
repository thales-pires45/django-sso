import json
from django.contrib.messages import constants
from django.contrib import messages, auth
from .models import Users as User
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')

    elif request.session.get("user"):
        return redirect('/auth/')

    else:
        status = request.GET.get('status')
        return render(request, 'login.html', {'status': status})


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Email ou senha não podem ficar vazior')
        return redirect('/auth/cadastro/')

    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve ter no mínimo 8 caracteres')
        return redirect('/auth/cadastro/')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse email')
        return redirect('/auth/cadastro/')

    if User.objects.filter(username=nome).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome')
        return redirect('/auth/cadastro/')

    try:

        usuario = User.objects.create_user(username=nome, email=email, password=senha)
        usuario.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
        return redirect('/auth/login/')

    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/auth/cadastro/')


def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    usuario = auth.authenticate(username=nome, password=senha)
    print(usuario)
    if not usuario:
        messages.add_message(request, constants.WARNING, 'Email ou senha inválido')
        return redirect('/auth/login/')
    else:
        auth.login(request, usuario)
        return redirect('/plataforma/home')


def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    return redirect('/auth/login/')


def login_auth0(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar a plataforma')
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def index(request):
    return render(
        request,
        "home.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
