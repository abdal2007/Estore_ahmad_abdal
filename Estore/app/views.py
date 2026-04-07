from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.
class ProductAPI(APIView):
    # Post-Method
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    # Get-Method
    #helper function
    def get_object(self,id):
        return get_object_or_404(Product,id=id)

    def get(self,request, id=None, min_price=None, max_price=None):

        # Agar range di ho
        if min_price is not None and max_price is not None:
            products = Product.objects.filter(
                price__gte=min_price,
                price__lte=max_price
            )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        
        # Agar ID di ho → single product

        if id is not None:
            # try:
            #     products = Product.objects.get(id=id)
            # except Product.DoesNotExist:
            #     raise Http404("Product not found")
            
            products = self.get_object(id)
            serializer = ProductSerializer(products)
            return Response(serializer.data)
        
        # Agar ID na ho → sab product
        products=Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
