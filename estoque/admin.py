from django.contrib import admin
from .models import Perfil, Produto, Categoria, Depositos, Movimentacao
# Register your models here.

admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Depositos)
admin.site.register(Movimentacao)
admin.site.register(Perfil)
