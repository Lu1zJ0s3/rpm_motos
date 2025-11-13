
from rest_framework import serializers
from produtos.models import Categoria, Marca, Produto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'ativo']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome', 'pais_origem', 'logo']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'categoria', 'marca',
            'modelo', 'ano', 'cilindrada', 'cor', 'preco', 'preco_promocional',
            'estoque', 'estoque_minimo', 'codigo_barras', 'imagem_principal',
            'ativo', 'destaque', 'data_cadastro', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_cadastro', 'data_atualizacao']
