from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.redirecionar, name="redirecionar_perfil" ),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produtos/", views.produtos, name="produtos"),
    path("produtos/cadastrar/", views.cadastrar_produto, name="cadastrar_produto"),
    path("produtos/editar/<int:produto_id>/", views.editar_produto, name="editar_produto"),
    path("produtos/excluir/<int:produto_id>/", views.excluir_produto, name="excluir_produto"),
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
    path("saida/", views.saida, name="saida"),
    path("relatorios/", 
         views.relatorio_produtos,
         name="relatorio_produtos"
),
]