
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from vendas.models import Venda, Cliente, Faturamento
from .serializers import (
    VendaSerializer,
    ClienteSerializer,
    FaturamentoSerializer
)

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['cliente', 'vendedor', 'status', 'data_venda']
    search_fields = ['numero_venda', 'cliente__nome', 'vendedor__username']
    ordering_fields = ['data_venda', 'total', 'numero_venda']
    ordering = ['-data_venda']
    def get_serializer_class(self):
        return VendaSerializer
    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'ativo', 'estado']
    search_fields = ['nome', 'cpf_cnpj', 'email']
    ordering_fields = ['nome', 'data_cadastro']
    ordering = ['nome']

class FaturamentoViewSet(viewsets.ModelViewSet):
    queryset = Faturamento.objects.all()
    serializer_class = FaturamentoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if not self.request.user.is_proprietario:
            return Faturamento.objects.none()
        return Faturamento.objects.all()
