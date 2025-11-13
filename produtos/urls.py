from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [

    path('', views.lista_produtos, name='lista'),
    path('novo/', views.criar_produto, name='criar'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe'),
    path('<int:pk>/editar/', views.editar_produto, name='editar'),
    path('estoque/', views.estoque_produtos, name='estoque'),

]
