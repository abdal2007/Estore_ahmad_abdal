from django.urls import path
from .views import ProductAPI#,ProductPriceRangeAPI


urlpatterns = [
    path('products/',ProductAPI.as_view()),
    path('products/<int:id>/',ProductAPI.as_view()),#by id
    path('products/range/',ProductAPI.as_view()), #rangee
    

]