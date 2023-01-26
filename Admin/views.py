from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.models import User
from .utils import *
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required()
def HomePage(request):
    page_title = 'dashboard'
    products = Product.objects.all().order_by('-date')
    categories = Category.objects.all()
    ads = AD.objects.filter(status='approved')
    users = User.objects.all()

    context = {
        'product_num': products.count(),
        'product': products,
        'category': categories.count(),
        'ad': ads.count(),
        'user': users.count(),
        # product monthly num
        'pm': getDataByDate(Product, 'monthly', 'date'),
        # ads monthly num
        'am': getDataByDate(AD, 'monthly', 'date'),
        # users monthly num
        'um': getDataByDate(User, 'monthly', 'date_joined'),
        'page_title': page_title
    }

    return render(request, 'pages/home.html', context=context)


@login_required()
def ProductsPage(request):
    page_title = 'products'

    products = Product.objects.all().order_by('-date')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }

    return render(request, 'pages/products.html', context)


@login_required()
def EditProductPage(request, pk):
    page_title = 'edit product'
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':

        print(request.POST)

        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

        data = request.POST
        newData = {}
        for k, v in dict(data).items():
            newData[k] = v[0]
        fields_to_remove = ('user', 'expire_date', 'status',
                            'category', 'subCategory', 'csrfmiddlewaretoken')
        for i in fields_to_remove:
            newData.pop(i)
        product.fields = newData
        product.save()

        return redirect('products')

    context = {
        'product': product,
        'form': form,
        'page_title': page_title
    }

    return render(request, 'pages/edit_product.html', context)


@login_required()
def UsersPage(request):
    page_title = 'users'
    user = User.objects.all()
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }
    return render(request, 'pages/users.html', context)


@login_required()
def EditUserPage(request, pk):
    page_title = 'edit user'
    user = get_object_or_404(User, id=pk)
    products = Product.objects.filter(user=user)

    if request.method == 'POST':
        data = request.POST

        if not User.objects.filter(username=data['username']).exists():
            # To do
            # Send Notification user with that Username already exsits....
            user.username = data['username']

        user.first_name = data['name']
        user.last_name = data['contact']
        if not User.objects.filter(email=data['email']).exists():
            # To do
            # Send Notification user with that Email already exsits....
            user.email = data['email']

        if len(data['password']) >= 6:
            user.set_password(data['password'])

        user.save()

        return redirect('users')

    context = {
        'user': user,
        'page_title': page_title,
        'product': products
    }
    return render(request, 'pages/edit_user.html', context)


@login_required()
def CategoryPage(request):
    page_title = 'categories'
    categories = Category.objects.all().order_by('name')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }

    return render(request, 'pages/categories.html', context)


@login_required()
def EditCategoryPage(request, pk):
    page_title = 'edit category'
    category = get_object_or_404(Category, id=pk)

    if request.method == 'POST':
        data = request.POST
        category.name = data['name']
        category.status = data['status']
        category.save()

        return redirect('category')

    context = {
        'category': category,
        'page_title': page_title
    }

    return render(request, 'pages/edit_category.html', context)


@login_required()
def deleteCategory(request, pk, F):
    page_title = 'page_title'
    category = get_object_or_404(Category, id=pk)

    if F != 0:
        type = 'deleteField'
        data = {'categoryId': pk, 'field': F}
    else:
        type = 'deleteCategory'
        data = {'categoryId': pk}

    if request.method == 'POST':
        category.fields.pop(F)
        category.save()
        return redirect('edit_category', pk=category.id)

    context = {
        'type': type,
        'data': data,
        'page_title': page_title
    }

    return render(request, 'pages/delete.html', context)


@login_required()
def ADPages(request):
    page_title = 'ads'
    ads = AD.objects.all()
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }
    return render(request, 'pages/ads.html', context)


@login_required()
def EditAdPage(request, pk):
    page_title = 'edit ad'
    ad = get_object_or_404(AD, id=pk)
    form = ADForm(instance=ad)

    if request.method == 'POST':
        form = ADForm(request.POST)
        if form.is_valid():
            ad.name = form.cleaned_data['name']
            ad.status = form.cleaned_data['status']
            ad.photo = form.cleaned_data['photo']
            ad.expire_date = form.cleaned_data['expire_date']
            ad.contact = form.cleaned_data['contact']

            ad.save()

            return redirect('ads')
        else:
            return redirect('ads')
    context = {
        'ad': ad,
        'form': form,
        'page_title': page_title
    }

    return render(request, 'pages/edit_ad.html', context)


@login_required()
def AddNewAD(request):
    page_title = 'add new ad'
    if request.method == 'POST':
        form = ADForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ads')
        else:
            print(form.errors.as_text)
            return redirect('ads')

    else:
        form = ADForm()

    context = {
        'form': form,
        'page_title': page_title
    }

    return render(request, 'pages/new_ad.html', context)


@login_required()
def AddNewCategory(request):
    page_title = 'add new category'
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            if not Category.objects.filter(name=form.cleaned_data['name']).exists():
                form.save()
            return redirect('category')
        else:
            return redirect('category')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'page_title': page_title
    }
    return render(request, 'pages/new_category.html', context)


@login_required()
def SubCategoryPage(request):
    page_title = 'subcategory'
    sub = SubCategory.objects.all().order_by('-id')
    paginator = Paginator(sub, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }
    return render(request, 'pages/sub.html', context)


@login_required()
def EditSubCategory(request, pk):
    page_title = 'edit subcategory'
    sub = get_object_or_404(SubCategory, id=pk)
    form = SubCategoryForm(instance=sub)

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            sub.name = form.cleaned_data['name']
            sub.mainCategory = form.cleaned_data['mainCategory']

            sub.save()

            return redirect('sub')
        else:
            return redirect('sub')
    context = {
        'sub': sub,
        'form': form,
        'page_title': page_title
    }

    return render(request, 'pages/edit_sub.html', context)


@login_required()
def AddNewSubCategory(request):
    page_title = 'add new subcategory'
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)

        if form.is_valid():
            if not SubCategory.objects.filter(name=form.cleaned_data['name']).exists():
                form.save()
            return redirect('sub')
        else:
            return redirect('sub')
    else:
        form = SubCategoryForm()

    context = {
        'form': form,
        'page_title': page_title
    }
    return render(request, 'pages/new_sub.html', context)


@login_required()
def AboutPage(request):
    page_title = 'about'
    about = About.objects.get(id=1)

    if request.method == 'POST':
        form = AboutForm(request.POST)
        if form.is_valid():
            about.about_us = form.cleaned_data['about_us']
            about.contact_number = form.cleaned_data['contact_number']
            about.whatsapp_number = form.cleaned_data['whatsapp_number']
            about.payment_info_text = form.cleaned_data['payment_info_text']
            about.payment_info_link = form.cleaned_data['payment_info_link']
            about.app_name = form.cleaned_data['app_name']
            about.auto_approve = form.cleaned_data['auto_approve']

            about.save()
    else:
        form = AboutForm(instance=about)

    context = {
        'form': form,
        'page_title': page_title
    }

    return render(request, 'pages/about.html', context)


@login_required()
def agreementPage(request):
    about = About.objects.get(id=1)
    data = request.POST
    context = {
        'text': about.agree_text
    }
    if request.method == 'POST':
        if 'agree' in data:
            agreementText = data['agree']

            about.agree_text = agreementText

            about.save()

            return redirect('agree')
        else:
            print('bad data')
    return render(request, 'pages/agree.html', context)


@login_required()
def privacyPage(request):
    about = About.objects.get(id=1)
    data = request.POST
    context = {
        'text': about.privacy_policy
    }
    if request.method == 'POST':
        if 'privacy' in data:
            privacyText = data['privacy']

            about.privacy_policy = privacyText

            about.save()

            return redirect('privacy')
        else:
            print('bad data')
            return redirect('privacy')
    return render(request, 'pages/privacy.html', context)
