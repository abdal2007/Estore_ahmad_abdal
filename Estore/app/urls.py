from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('products/',ProductAPI.as_view()),
    path('products/<int:id>/',ProductAPI.as_view()),#by id
    path('products/range/',ProductAPI.as_view()), #rangee
    path('category/',CategoryAPI.as_view()),
    path('category/<int:id>',CategoryAPI.as_view()),
    path('category/<int:id>',CategoryAPI.as_view()),
    path('products/category/<int:category_id>',ProductByCategoryAPI.as_view()),
    path('login/',LoginAPI.as_view()), 
    path('signup/',SignUpAPI.as_view()),
    #JWT
    # path('api/login/', TokenObtainPairView.as_view(), name='login'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),


    path('logout/', LogoutAPI.as_view()),
    # path('send-otp/', SendOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('products/<int:pk>/add-review/', AddReviewAPI.as_view()),
    path('products/<int:pk>/reviews/', ProductReviewAPI.as_view()),
    path('products/search/', ProductSearchAPI.as_view()),


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)