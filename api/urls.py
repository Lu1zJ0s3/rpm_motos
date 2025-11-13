from rest_framework.routers import DefaultRouter
from produtos.api.views import ProdutoViewSet, CategoriaViewSet, MarcaViewSet
from usuarios.api.views import UsuarioViewSet
from vendas.api.views import VendaViewSet, ClienteViewSet, FaturamentoViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'faturamento', FaturamentoViewSet)

urlpatterns = router.urls
