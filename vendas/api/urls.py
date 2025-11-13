
from rest_framework.routers import DefaultRouter
from .views import VendaViewSet, ClienteViewSet, FaturamentoViewSet

router = DefaultRouter()
router.register(r'vendas', VendaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'faturamento', FaturamentoViewSet)

urlpatterns = router.urls
