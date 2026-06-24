from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
        
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
    
class Depositos(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Movimentacao(models.Model):
    TIPOS = (
        ("E", "Entrada"),
        ("S", "Saída"),
    )

    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    deposito = models.ForeignKey("Depositos", on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    #usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"