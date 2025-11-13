
from rest_framework import serializers
from vendas.models import Cliente, Venda, Faturamento

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'tipo', 'cpf_cnpj', 'email', 'telefone',
            'endereco', 'cidade', 'estado', 'cep', 'data_cadastro', 'ativo'
        ]
        read_only_fields = ['id', 'data_cadastro']

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = [
            'id', 'numero_venda', 'cliente', 'vendedor', 'data_venda',
            'status', 'forma_pagamento', 'subtotal', 'desconto', 'total',
            'observacoes'
        ]
        read_only_fields = ['id', 'numero_venda', 'vendedor', 'data_venda', 'subtotal', 'total']

class FaturamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faturamento
        fields = [
            'id', 'data', 'vendas_dia', 'faturamento_bruto',
            'desconto_total', 'faturamento_liquido', 'lucro_estimado'
        ]
        read_only_fields = ['id']
