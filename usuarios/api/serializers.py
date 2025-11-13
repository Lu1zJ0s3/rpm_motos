
from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'tipo_usuario', 'telefone',
            'endereco', 'data_nascimento', 'cpf'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class UsuarioLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Usuário está inativo.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Credenciais inválidas.")
        else:
            raise serializers.ValidationError("Username e password são obrigatórios.")
        return data

class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'telefone', 'endereco', 'data_nascimento',
            'cpf', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
