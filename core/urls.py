from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.addNewProduct),
    path('product/get/user/', views.getUserProducts),
    path('product/get/id/', views.getProductbyId),
    path('product/get/category/', views.getProductByCat),
    path('product/get/category/sub/', views.getProductBySubCat),
    path('product/update/fields/', views.updateProdcutFields),
    path('product/update/status', views.updateProductStatus),
    path('prodcut/update/expire/', views.updateProductExpireDate),

    path('user/login/', views.Login),
    path('user/register/', views.Register),
    path('user/password/change/', views.ChangePassword),
    path('user/update/', views.updateUser),
    path('category/get/fields/', views.getCategoryFields),
    path('category/get/all/', views.getCategories),

    path('category/sub/get/id/', views.getSubCategoryById),
    path('category/sub/get/all/', views.getAllSubCategories),

    path('about/', views.AboutApi),
]
