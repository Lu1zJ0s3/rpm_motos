
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, CategoriaViewSet, MarcaViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)

urlpatterns = router.urls
