from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('product/create', views.addNewProduct),
    path('product/get/user', views.getUserProducts),
    path('product/get/id', views.getProductbyId),
    path('product/get/category', views.getProductByCat),
    path('product/get/category/sub', views.getProductBySubCat),
    path('product/update/fields', views.updateProdcutFields),
    path('product/update/status', views.updateProductStatus),
    path('product/update/expire', views.updateProductExpireDate),
    path('product/update/photos', views.updateProductPhotos),
    path('product/get/comments', views.getProductComments),
    path('product/comment', views.Productcomment),
    path('product/get/all', views.getAllProducts),
    path('product/comment/replay', views.CommentReplayView),
    path('user/login', views.Login),
    path('user/register', views.Register),
    path('user/password/change', views.ChangePassword),
    path('user/update', views.updateUser),
    path('user/get/details', views.getUserDetails),

    path('category/get/fields', views.getCategoryFields),
    path('category/get/all', views.getCategories),
    path('category/get/id', views.getCategory),

    path('category/sub/get/id', views.getSubCategoryById),
    path('category/sub/get/all', views.getAllSubCategories),


    path('about', views.AboutApi),

    path('ads', views.ADS),

    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('user/notifications', views.UserNotifications)

]
