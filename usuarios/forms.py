from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario
import re


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite seu usuário',
            'required': 'required',
            'id': 'id_username'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite sua senha',
            'required': 'required',
            'id': 'id_password'
        })
    )
    
    remember_me = forms.BooleanField(
        label='Lembrar de mim',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded',
            'id': 'remember_me'
        })
    )

    error_messages = {
        'invalid_login': 'Nome de usuário ou senha incorretos.',
        'inactive': 'Esta conta está inativa.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label_suffix = ''
        self.fields['password'].label_suffix = ''


class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite seu nome',
            'id': 'id_first_name'
        })
    )
    
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite seu sobrenome',
            'id': 'id_last_name'
        })
    )
    
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        required=True,
        help_text='Obrigatório. 150 caracteres ou menos. Apenas letras, números e @/./+/-/_ permitidos.',
        widget=forms.TextInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite seu usuário',
            'id': 'id_username'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite seu email',
            'id': 'id_email'
        })
    )
    
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': '000.000.000-00',
            'id': 'id_cpf'
        })
    )
    
    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': '(11) 99999-9999',
            'id': 'id_telefone'
        })
    )
    
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Digite sua senha',
            'id': 'id_password1'
        }),
        help_text='Sua senha deve conter pelo menos 8 caracteres.'
    )
    
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'class': 'pl-10 block w-full border border-gray-300 rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Confirme sua senha',
            'id': 'id_password2'
        })
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'username', 'email', 'cpf', 'telefone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_suffix = ''

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = re.sub(r'\D', '', cpf)
            
            if len(cpf) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')
            
            if cpf == cpf[0] * 11:
                raise ValidationError('CPF inválido.')
            
            def calcular_digito(cpf_parcial, peso_inicial):
                soma = sum(int(digito) * peso for digito, peso in zip(cpf_parcial, range(peso_inicial, 1, -1)))
                resto = soma % 11
                return '0' if resto < 2 else str(11 - resto)
            
            digito1 = calcular_digito(cpf[:9], 10)
            if cpf[9] != digito1:
                raise ValidationError('CPF inválido.')
            
            digito2 = calcular_digito(cpf[:10], 11)
            if cpf[10] != digito2:
                raise ValidationError('CPF inválido.')
            
            if Usuario.objects.filter(cpf=cpf).exists():
                raise ValidationError('Este CPF já está cadastrado.')
            
            return cpf
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError('Este email já está cadastrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if Usuario.objects.filter(username=username).exists():
                raise ValidationError('Este nome de usuário já existe.')
        return username

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = re.sub(r'\D', '', telefone)
            if len(telefone) not in [10, 11]:
                raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
            if len(telefone) == 11:
                return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
            else:
                return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        return telefone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.cpf = self.cleaned_data['cpf']
        user.telefone = self.cleaned_data['telefone']
        user.tipo_usuario = 'vendedor'  
        
        if commit:
            user.save()
        return user


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone', 'endereco', 'data_nascimento']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '(11) 99999-9999'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_suffix = ':'
            if self.fields[field].label:
                self.fields[field].label = self.fields[field].label.title()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.instance:
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este email já está cadastrado.')
        return email