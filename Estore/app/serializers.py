from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

    #price validator
    def validate_price(self,value):
        if value<0:
            raise serializers.ValidationError("Product price must be positive")
        return value
    # title validator
    def validate_title(self, value):
        if len(value)<3:
            raise serializers.ValidationError("Title should be more than 3 characters long")
        return value
    
    #description validator
    def validate_description(self, value):
        if len(value)<10:
            raise serializers.ValidationError("Product Description should be more than 10 characters long! ")
        return value
    

    
