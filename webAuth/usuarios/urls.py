from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('valida_cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('sair/', views.sair, name='sair'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path("login_auth0/", views.login_auth0, name="login_auth0"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("", views.index, name="index"),
]
