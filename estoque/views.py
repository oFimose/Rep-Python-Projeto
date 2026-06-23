from django.shortcuts import render, redirect
from .models import Produto, Categoria, Depositos, Movimentacao

# Create your views here.
def dashboard(request):
    return render(request, "dashboard_adm.html")


def login_view(request):
    return render(request, "login.html")

def produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'produtos.html', {'produtos': produtos})
    
def cadastrar_produto(request):
    if request.method == "POST":

        categoria = Categoria.objects.get(
            id=request.POST["categoria"]
        )
        Produto.objects.create(
            nome=request.POST["nome"],
            descricao=request.POST["descricao"],
            quantidade=request.POST["quantidade"],
            categoria=categoria
        )
        return redirect("produtos")
    
    categorias = Categoria.objects.all()
    return render(request, "cadastrar_produto.html", {"categorias": categorias})
    
def cadastrar_categoria(request):
    if request.method == "POST":
        Categoria.objects.create(
            nome=request.POST["nome"],
            descricao=request.POST["descricao"]
        )
        return redirect("cadastrar_produto")
    return render(request, "cadastrar_categoria.html")

def depositos(request):
    depositos = Depositos.objects.all()

    return render(request, 'depositos.html', {'depositos': depositos})

def cadastrar_deposito(request):
    if request.method == "POST":
        Depositos.objects.create(
            nome=request.POST["nome"],
            localizacao=request.POST["localizacao"],
            responsavel=request.POST["responsavel"]
        )
        return redirect("depositos")
    return render(request, "cadastrar_deposito.html")

def entrada(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))
        observacao = request.POST.get('observacao')

        produto = Produto.objects.get(id=produto_id)

        Movimentacao.objects.create(
            produto=produto,
            quantidade=quantidade,
            tipo="E",
            observacao=observacao
        )

        produto.quantidade += quantidade
        produto.save()

        return redirect('entrada')
    
    entradas = Movimentacao.objects.filter(tipo="E").order_by("-data")
    produtos = Produto.objects.all()

    return render(request, 'entrada.html', {
        'entradas': entradas,
        'produtos': produtos
    })

def saida(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))
        observacao = request.POST.get('observacao')

        produto = Produto.objects.get(id=produto_id)

        if quantidade <= produto.quantidade:
            Movimentacao.objects.create(
                produto=produto,
                quantidade=quantidade,
                tipo="S",
                observacao=observacao
            )

            produto.quantidade -= quantidade
            produto.save()

        return redirect('saida')
    
    saidas = Movimentacao.objects.filter(tipo="S").order_by("-data")
    produtos = Produto.objects.all()
    
    return render(request, "saida.html", {
        "saidas": saidas,
        "produtos": produtos
    })