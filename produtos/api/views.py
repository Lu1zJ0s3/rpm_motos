
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from produtos.models import Produto, Categoria, Marca
from .serializers import (
    ProdutoSerializer,
    CategoriaSerializer,
    MarcaSerializer
)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'marca', 'ativo']
    search_fields = ['nome', 'descricao', 'modelo']
    ordering_fields = ['nome', 'preco', 'data_cadastro']
    ordering = ['-data_cadastro']
    
    def get_serializer_class(self):
        return ProdutoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
