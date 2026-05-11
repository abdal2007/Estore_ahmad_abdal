from rest_framework import serializers
from .models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

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

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'product', 'created_at']
            
    

    
