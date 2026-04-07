from django.urls import path
from .views import ProductAPI


urlpatterns = [
    path('products/',ProductAPI.as_view()),
    path('products/<int:id>/',ProductAPI.as_view()),
    path('products/<int:min_price>-<int:max_price>/',ProductAPI.as_view()), #rangee
]