from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .models import Product, Category, OTP
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from .utils import generate_otp
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import AllowAny, BasePermission
# Create your views here.

# permission--------------------------------------------------------------
class IsAuthenticatedOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated
  
# APIView for Product and Category=======================================================
class ProductAPI(APIView):

    #permission-----------------------------------------------------------------------
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticatedOrCreateOnly()]
    
    
    # Post-Method------------------------------------------------------------------------------
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
     #helper function-------------------------------------------------------------------------
    def get_object(self,id):
        return get_object_or_404(Product,id=id)

    #PUT-Method---------------------------------------------------------------------------------
    def put(self,request,id):
        products=self.get_object(id)
        serializers=ProductSerializer(products,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Patch-Method---------------------------------------------------------------------------------
    def patch(self,request,id):
        products=self.get_object(id)
        serializers=ProductSerializer(products,data=request.data, partial= True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Delete-Method------------------------------------------------------------------------------
    def delete(self,request, id):
        products=self.get_object(id)
        
        products.delete()
        return Response({"message":"Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        



    # Get-Method----------------------------------------------------------------------------------
   

    def get(self,request, id=None):

        # Agar ID di ho → single product
        
        if id is not None:

            try:
                products = Product.objects.get(id=id)
            except Product.DoesNotExist:
                raise Http404("Product not found")
            
            products = self.get_object(id)
            serializer = ProductSerializer(products)
            return Response(serializer.data)

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        products = Product.objects.all()
        
        if min_price and max_price:
            products=Product.objects.filter(price__range=(min_price,max_price))
        elif min_price:
            products=Product.objects.filter(price__gte=min_price)
        elif max_price:
            products=Product.objects.filter(price__lte=max_price)
           
        if not products.exists():
            raise NotFound("No products found in this price range")
        

        serializers =ProductSerializer(products, many=True)     
        return Response(serializers.data)
    
        
class CategoryAPI(APIView):

    #permission-----------------------------------------------------------------------
    def permission_classes(self):
            if self.request.method == 'GET':
                return [AllowAny()]
            return [IsAuthenticatedOrCreateOnly()]
    # Post-Method------------------------------------------------------------------------------
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
     #helper function-------------------------------------------------------------------------
    def get_object(self,id):
        return get_object_or_404(Category,id=id)

    #PUT-Method---------------------------------------------------------------------------------
    def put(self,request,id):
        category=self.get_object(id)
        serializers=CategorySerializer(category,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Patch-Method---------------------------------------------------------------------------------
    def patch(self,request,id):
        category=self.get_object(id)
        serializers=CategorySerializer(category,data=request.data, partial= True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Delete-Method------------------------------------------------------------------------------
    def delete(self,request, id):
        category=self.get_object(id)
        
        category.delete()
        return Response({"message":"Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        



    # Get-Method----------------------------------------------------------------------------------
   

    def get(self,request, id=None):

        # Agar ID di ho → single product
        if id is not None:
            try:
                category = Category.objects.get(id=id)
            except Category.DoesNotExist:
                raise Http404("Product not found")
            
            # category = self.get_object(id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        
        category= Category.objects.all()
        serializers =CategorySerializer(category, many=True)     
        return Response(serializers.data)        

# Get products by category API ========================================================
class ProductByCategoryAPI(APIView):
    def get(self, request, category_id):
        category=get_object_or_404(Category, id=category_id)

        products = Product.objects.filter(category=category)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        
#login API ========================================================
class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error":"Email and Password require"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=email, password=password)
                    
        if user is not None:
                
            if not user.is_active:
                return Response(
                    {"error": "Account not verified"},
                    status=status.HTTP_403_FORBIDDEN
                    
                )
            login(request, user)
            return Response(
                {"Message":"Login successfull"},
                status=status.HTTP_200_OK )
        return Response(
            {"error":"Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )
#signup API ========================================================    
class SignUpAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        # OTP generate
        otp = generate_otp()
        OTP.objects.create(user=user, code=otp)

        #  SEND EMAIL
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return Response({
            "message": "Signup successful. OTP sent to email."
        }, status=201)
    
# Logout API ========================================================
class LogoutAPI(APIView):
    

    def post(self, request):
        logout(request)  # session destroy

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
            
# class SendOTP(APIView):
#     def post(self, request):
#         email = request.data.get('email')

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=404)

#         OTP.objects.filter(user=user).delete()

#         otp = generate_otp()
#         OTP.objects.create(user=user, code=otp)

#             # SEND EMAIL
#         send_mail(
#             subject='Your OTP Code',
#             message=f'Your OTP is: {otp}',
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         return Response({'message': 'OTP sent to email'})
                
# Verify OTP API ========================================================
class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, code=code).last()
        except:
            return Response({'error': 'Invalid OTP'}, status=400)

        if not otp:
             return Response({'error': 'Invalid OTP'}, status=400)

            # expiry check (5 minutes)
        if otp.created_at < timezone.now() - timedelta(minutes=30):
            return Response({'error': 'OTP expired'}, status=400)

        otp.is_verified = True
        otp.save()

        return Response({'message': 'OTP verified'})
        
# Resend OTP API ========================================================            
class ResendOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "Email required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try: 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
            
        otp_code = OTP.generate_otp()    

        OTP.objects.filter(user=user).delete()
        OTP.objects.create(user=user, code=otp_code)

        send_mail(
            subject="Your New OTP",
            message=f"Your new OTP is {otp_code}",
            from_email=None,
            recipient_list=[email],
        )
        return Response({"message": "OTP resent successfully"})
        
# Reset Password API ========================================================
class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, is_verified=False).last()
        except:
            return Response({'error': 'Invalid request'}, status=400)

        if not otp:
            return Response({'error': 'OTP not verified'}, status=400)

        user.set_password(new_password)
        user.save()

            # delete OTP after use
        OTP.objects.filter(user=user).delete()

        return Response({'message': 'Password reset successful'})

#Reviews==============================
class AddReviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        

        # check if already reviewed
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "You already reviewed this product"}, status=400)
        
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
# Get reviews for a product API ========================================================    
class ProductReviewAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # related_name='reviews' 
        reviews = product.reviews.all().order_by('-created_at')

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# Product Search API ========================================================

class ProductSearchAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


