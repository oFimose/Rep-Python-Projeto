from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produtos/", views.produtos, name="produtos"),
    path("produtos/cadastrar/", views.cadastrar_produto, name="cadastrar_produto"),
    path(
        "categorias/cadastrar/",
        views.cadastrar_categoria,
        name="cadastrar_categoria"
    ),
    path("depositos/", views.depositos, name="depositos"),
    path(
        "depositos/cadastrar/",
        views.cadastrar_deposito,
        name="cadastrar_deposito"
    ),
    path("entrada/", views.entrada, name="entrada"),
    path("saida/", views.saida, name="saida")
]