from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Produto, Categoria, Marca
from .forms import ProdutoForm


@login_required
def lista_produtos(request):

    produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.filter(ativo=True)
    marcas = Marca.objects.all()

    categoria_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')
    search = request.GET.get('search')

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    elif marca_id:
        produtos = produtos.filter(marca_id=marca_id)
    elif search:
        produtos = produtos.filter(nome__icontains=search)

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'marcas': marcas,
        'titulo': 'Produtos - RPM Motos'
    }
    return render(request, 'produtos/lista.html', context)

@login_required
def detalhe_produto(request, pk):

    produto = get_object_or_404(Produto, pk=pk)
    context = {
        'produto': produto,
        'titulo': f'{produto.nome} - RPM Motos'
    }
    return render(request, 'produtos/detalhe.html', context)

@login_required
def criar_produto(request):

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('produtos:detalhe', pk=produto.pk)
    else:
        form = ProdutoForm()

    context = {
        'form': form,
        'titulo': 'Novo Produto - RPM Motos'
    }
    return render(request, 'produtos/form.html', context)

@login_required
def editar_produto(request, pk):

    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtos:detalhe', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)

    context = {
        'form': form,
        'produto': produto,
        'titulo': f'Editar {produto.nome} - RPM Motos'
    }
    return render(request, 'produtos/form.html', context)

@login_required
def estoque_produtos(request):

    produtos = Produto.objects.all().order_by('nome')
    categorias = Categoria.objects.filter(ativo=True)

    produtos_em_estoque = produtos.filter(estoque__gt=0).count()
    produtos_estoque_baixo = produtos.filter(estoque__lte=F('estoque_minimo'), estoque__gt=0).count()
    produtos_sem_estoque = produtos.filter(estoque=0).count()

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'produtos_em_estoque': produtos_em_estoque,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'produtos_sem_estoque': produtos_sem_estoque,
        'titulo': 'Controle de Estoque - RPM Motos'
    }
    return render(request, 'produtos/estoque.html', context)
