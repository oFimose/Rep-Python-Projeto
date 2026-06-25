from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Produto, Categoria, Depositos, Movimentacao, Perfil

# Create your views here.
@login_required
def redirecionar(request):
    try: 
        perfil = request.user.perfil
        if perfil.tipo == "ADMIN":
            return redirect('dashboard')
        else:
            return redirect('produtos')
    except Perfil.DoesNotExist:
        return redirect("login")

@login_required
def dashboard(request):
    total_produtos = Produto.objects.count()
    total_entradas = Movimentacao.objects.filter(tipo="E").count()
    total_saidas = Movimentacao.objects.filter(tipo="S").count()
    ultimas_movs = Movimentacao.objects.order_by("-data")[:5]
    context = {
        'total_produtos': total_produtos,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'ultimas_movs': ultimas_movs,
    }
    return render(request, "dashboard_adm.html", context)

@login_required
def produtos(request):
    busca = request.GET.get("busca", "").strip()
    categoria_id = request.GET.get("categoria", "")
    produto_consultar = Produto.objects.all()
    if busca:
        produto_consultar = produto_consultar.filter(nome__icontains=busca)
    if categoria_id:
        produto_consultar = produto_consultar.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    context = {
        'produtos': produto_consultar,
        'categorias': categorias,
        'busca_atual': busca,
        'categoria_atual': categoria_id,
    }
    return render(request, 'produtos.html', context)

@login_required
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

@login_required
def editar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return redirect("produtos")
    categorias = Categoria.objects.all()

    if request.method == "POST":
        produto.nome = request.POST.get("nome")
        produto.descricao = request.POST.get("descricao")
        produto.quantidade = request.POST.get("quantidade")
        categoria_id = request.POST.get("categoria")
        if categoria_id:
            produto.categoria_id = categoria_id
        else:
            produto.categoria = None
        produto.save()
        return redirect("produtos")
    return render(request, "cadastrar_produto.html", {
        'produto': produto,
        'categorias': categorias,
        'modo_edicao': True
    })

@login_required
def excluir_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return redirect("produtos")
    
    if request.method == "POST":
        produto.delete()
    
    return redirect("produtos")

@login_required
def cadastrar_categoria(request):
    next_url = request.GET.get("next")
    if request.method == "POST":
        Categoria.objects.create(
            nome=request.POST["nome"],
            descricao=request.POST.get("descricao", "")
        )
        if next_url == "fechar":
            return HttpResponse("<script>window.close();</script>")
        
        return redirect(next_url if next_url else "cadastrar_produto")
    return render(request, "cadastrar_categoria.html")

@login_required
def depositos(request):
    depositos = Depositos.objects.all()

    return render(request, 'depositos.html', {'depositos': depositos})

@login_required
def cadastrar_deposito(request):
    if request.method == "POST":
        Depositos.objects.create(
            nome=request.POST["nome"],
            localizacao=request.POST["localizacao"],
            responsavel=request.POST["responsavel"]
        )
        return redirect("depositos")
    return render(request, "cadastrar_deposito.html")

@login_required
def entrada(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))
        observacao = request.POST.get('observacao')
        deposito_id = request.POST.get('deposito')  

        produto = Produto.objects.get(id=produto_id)
        deposito = None
        if deposito_id:
            deposito = Depositos.objects.get(id=deposito_id)

        Movimentacao.objects.create(
            produto=produto,
            deposito=deposito,  
            quantidade=quantidade,
            tipo="E",
            observacao=observacao
        )

        produto.quantidade += quantidade
        produto.save()

        return redirect('entrada')
    
    entradas = Movimentacao.objects.filter(tipo="E").order_by("-data")
    produtos = Produto.objects.all()
    depositos = Depositos.objects.all()
    return render(request, 'entrada.html', {
        'entradas': entradas,
        'produtos': produtos,
        'depositos': depositos
    })

@login_required
def saida(request):
    if request.method == "POST":
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))
        observacao = request.POST.get('observacao')
        deposito_id = request.POST.get('deposito')  

        produto = Produto.objects.get(id=produto_id)

        if quantidade <= produto.quantidade:
            deposito = None
            if deposito_id:
                deposito = Depositos.objects.get(id=deposito_id)

            Movimentacao.objects.create(
                produto=produto,
                deposito=deposito,  
                quantidade=quantidade,
                tipo="S",
                observacao=observacao
            )

            produto.quantidade -= quantidade
            produto.save()

        return redirect('saida')
    
    saidas = Movimentacao.objects.filter(tipo="S").order_by("-data")
    produtos = Produto.objects.all()
    depositos = Depositos.objects.all() 
    
    return render(request, "saida.html", {
        "saidas": saidas,
        "produtos": produtos,
        "depositos": depositos  
    })