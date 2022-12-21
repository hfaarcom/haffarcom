from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('about/', views.AboutPage, name='about'),

    path('products/', views.ProductsPage, name='products'),
    path('products/edit/<str:pk>/', views.EditProductPage, name='edit_product'),

    path('users/', views.UsersPage, name='users'),
    path('users/edit/<str:pk>/', views.EditUserPage, name='edit_user'),

    path('category/', views.CategoryPage, name='category'),
    path('category/edit/<str:pk>/', views.EditCategoryPage, name='edit_category'),
    path('category/delete/<str:pk>/<str:F>/', views.deleteCategory, name='delete_category'),
    path('category/new/', views.AddNewCategory, name='new_category'),
    path('category/sub/', views.SubCategoryPage, name='sub'),
    path('category/sub/edit/<str:pk>/', views.EditSubCategory, name='edit_sub'),
    path('category/sub/new/', views.AddNewSubCategory, name='new_sub'),

    path('ads/', views.ADPages, name='ads'),
    path('ads/edit/<str:pk>/', views.EditAdPage, name='edit_ad'),
    path('ads/new/', views.AddNewAD, name='new_ad'),


    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logoutUser')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    