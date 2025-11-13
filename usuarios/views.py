from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.db import models
from django.utils import timezone
from django.contrib import messages
from .forms import CustomLoginForm, CustomRegisterForm, EditarPerfilForm

@csrf_exempt
def registro_simples(request):
    from django.http import JsonResponse
    import json
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            return JsonResponse({'message': 'Usuário criado (simples, sem DRF)'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def login_simples(request):
    from django.http import JsonResponse
    import json
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            return JsonResponse({'message': 'Login realizado (simples, sem DRF)'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def home_page(request):

    return render(request, 'home.html')

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)  
                
                next_url = request.GET.get('next', 'usuarios:dashboard')
                messages.success(request, f'Bem-vindo de volta, {user.get_full_name() or user.username}!')
                return redirect(next_url)
        else:
            messages.error(request, 'Erro no login. Verifique seus dados.')
    else:
        form = CustomLoginForm()

    context = {
        'form': form,
        'titulo': 'Login - RPM Motos'
    }
    return render(request, 'registrar/login.html', context)

def custom_register_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.get_full_name()}!')
                login(request, user)
                return redirect('usuarios:dashboard')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados informados.')
    else:
        form = CustomRegisterForm()

    context = {
        'form': form,
        'titulo': 'Cadastro - RPM Motos'
    }
    return render(request, 'registrar/registrar.html', context)


def custom_logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta com sucesso.')
    return redirect('usuarios:login')
    return redirect('usuarios:home')

@login_required
def dashboard_usuario(request):

    from produtos.models import Produto
    from vendas.models import Venda
    from django.utils import timezone
    from datetime import datetime, timedelta

    total_produtos = Produto.objects.filter(ativo=True).count()
    total_vendas = Venda.objects.count()

    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    faturamento_mes = Venda.objects.filter(
        data_venda__gte=inicio_mes,
        status='concluida'
    ).aggregate(
        total=models.Sum('total')
    )['total'] or 0

    estoque_baixo = 0
    for produto in Produto.objects.filter(ativo=True):
        if produto.estoque < produto.estoque_minimo:
            estoque_baixo += 1

    ultimas_vendas = None
    produtos_destaque = None

    if request.user.is_proprietario:
        ultimas_vendas = Venda.objects.select_related('cliente').order_by('-data_venda')[:5]
        produtos_destaque = Produto.objects.filter(ativo=True).order_by('-data_cadastro')[:5]

    context = {
        'usuario': request.user,
        'titulo': 'Dashboard - RPM Motos',
        'total_produtos': total_produtos,
        'total_vendas': total_vendas,
        'faturamento_mes': f"{faturamento_mes:.2f}",
        'estoque_baixo': estoque_baixo,
        'ultimas_vendas': ultimas_vendas,
        'produtos_destaque': produtos_destaque,
    }
    return render(request, 'usuarios/dashboard.html', context)

@login_required
def perfil_view(request):

    context = {
        'usuario': request.user,
        'titulo': 'Meu Perfil - RPM Motos'
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil_view(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        data_nascimento = request.POST.get('data_nascimento')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.telefone = telefone
        user.endereco = endereco

        if data_nascimento:
            from datetime import datetime
            try:
                user.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                pass

        user.save()

        from django.contrib import messages
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('usuarios:perfil')

    context = {
        'usuario': request.user,
        'titulo': 'Editar Perfil - RPM Motos'
    }
    return render(request, 'usuarios/editar_perfil.html', context)

def teste_simples(request):

    from django.http import JsonResponse
    from django.utils import timezone
    return JsonResponse({
        'message': 'View simples funcionando!',
        'timestamp': timezone.now().isoformat()
    })
