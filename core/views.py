from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
import json
from datetime import date, timedelta


# Products
@api_view(['POST'])
def addNewProduct(request):
    try:
        data = request.data
        if {'user', 'category', 'fields'} <= set(data):
            # check POST data
            user = User.objects.get(id=data['user'])
            category = Category.objects.get(id=data['category'])
            fields = data['fields']
            expire_date = date.today() + timedelta(days=About.objects.get(id=1).product_expire_days)

            # convert STR to DICT/JSON
            Jfields = json.loads(fields)

            # check Product Fields
            if Jfields.keys() == category.fields.keys():

                # create New Product
                newProduct = Product.objects.create(
                    user=user, category=category, fields=Jfields, status='approved', expire_date=expire_date
                )

                # serialize data
                serializer = ProductsSerilizer(newProduct, many=False)

                # return data
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:

                return Response({'error': 'Product Fields Does not match with its category'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserProducts(request):
    try:
        data = request.query_params
        if 'user' in data:
            # get data + serialize it
            products = Product.objects.filter(user=data['user'])
            serializer = ProductsSerilizer(products, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProductByCat(request):
    try:
        data = request.query_params
        if 'category' in data:
            # check data + serialize it
            category = Category.objects.get(id=data['id'])
            products = Product.objects.filter(category=category)

            serializer = ProductsSerilizer(products, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProductBySubCat(request):
    try:
        data = request.query_params
        if 'subcategory' in data:
            # check data + serialize it
            category = SubCategory.objects.get(id=data['id'])
            products = Product.objects.filter(subCategory=category)

            serializer = ProductsSerilizer(products, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProductbyId(request):
    try:
        data = request.query_params
        if 'id' in data:
            # check data + serialize it
            product = Product.objects.get(id=data['id'])
            serializer = ProductsSerilizer(product, many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Bad Data'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateProdcut(request):
    try:
        data = request.data
        if {'product', 'fields'} <= set(data):
            # check data
            product = Product.objects.get(id=data['product'])
            category = Category.objects.get(id=product.category.id)

            # concert data from str to JSON

            Jfields = json.loads(data['fields'])

            # check given data fields and match it with its category
            if Jfields.keys() == category.fields.keys():
                # save data + serialize it
                product.fields = Jfields
                product.save()
                serializer = ProductsSerilizer(product, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Product Fields Does not match with its category'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# category
@api_view(['GET'])
def getCategoryFields(request):
    try:
        data = request.query_params
        # check given data
        if {'api_key', 'category'} <= set(data):
            if data['api_key'] == settings.API_KEY:
                # serialize data + return it
                category = Category.objects.get(id=data['category']).fields
                return Response(category, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Bad Data'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCategories(request):
    try:
        data = request.query_params
        if 'api_key' in data:
            if data['api_key'] == settings.API_KEY:
                # check data + serialize it
                category = Category.objects.all()
                serializer = CategorySerializer(category, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'API_KEY required'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# subcategory


@api_view(['GET'])
def getSubCategoryById(request):
    try:
        data = request.query_params
        if {'subcategory', 'api_key'} <= set(data):
            # check data + serialize it
            if data['api_key'] == settings.API_KEY:
                sub = SubCategory.objects.get(id=data['subcategory'])
                serializer = SubCategorySerializer(sub, many=False)

                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllSubCategories(request):
    try:
        data = request.query_params
        if 'api_key' in data:
            # check data + serialize it
            if data['api_key'] == settings.API_KEY:
                sub = SubCategory.objects.all()
                serializer = SubCategorySerializer(sub, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad bata'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Comments
@api_view(['GET'])
def getProductComments(request):
    try:
        data = request.query_params
        if 'product' in data:
            # check data + serialize it
            product = Product.objects.get(id=data['product'])
            comments = Comment.objects.filter(product=product)

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def newComment(request):
    try:
        data = request.data
        if {'user', 'description', 'product'} <= set(data):
            # check data + serialize it
            user = User.objects.get(id=data['user'])
            product = Product.objects.get(id=data['product'])
            description = data['description']

            comment = Comment.objects.create(
                user=user, product=product, description=description)

            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ADS


@api_view(['POST'])
def getADS(request):
    try:
        data = request.data
        if 'api_key' in data:
            if data['api_key'] == settings.API_KEY:
                # check data + serialize it
                ads = AD.objects.all()
                serializer = ADSerializer(ads)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# authentication


@api_view(['POST'])
def Login(request):
    try:
        data = request.data
        if {'email', 'password'} <= set(data):
            # check user
            username = data['username']
            password = data['password']
            # check if user exists
            if User.objects.filter(username=username).exists():
                # check if user authenticated
                auth = authenticate(
                    request, username=username, password=password)

                # serialize + return
                if auth is not None:
                    user = User.objects.get(username=username)
                    return Response({'user': user.id, 'username': user.username, 'first_name': user.first_name, 'contact': user.last_name, 'email': user.email}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'error': 'Username or Password are wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Username doesnt exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateUser(request):
    try:
        data = request.data
        if {'email', 'contact', 'name', 'user'} <= set(data):
            email = data['email']
            contact = data['contact']
            first_name = data['name']
            id = data['user']

            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
                user.email = email
                user.last_name = contact
                user.first_name = first_name

                user.save()

                return Response({'username': user.username, 'email': email, 'first_name': first_name, 'contact': contact, 'id': id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'user is not exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Register(request):
    try:
        data = request.data
        if {'username', 'password', 'email', 'name', 'contact'} <= set(data):
            # check data + serialize it
            username = data['username']
            first_name = data['name']
            email = data['email']
            contact = data['contact']
            # check if username and email are unique
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                newUser = User.objects.create_user(
                    username, email, data['password'])
                newUser.first_name = first_name
                # Last Name is the contact Number ...
                newUser.last_name = contact
                newUser.save()
                return Response({'username': username, 'email': email, 'first_name': first_name, 'contact': contact, 'id': newUser.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ChangePassword(request):
    try:
        data = request.data
        if {'username', 'oldpassword', 'newpassword'} <= set(data):
            username = data['username']
            # check if user authenticated
            user = authenticate(request, username=username,
                                password=data['oldpassword'])
            if user is not None:
                # set new password and save data
                newUser = User.objects.get(username=username)
                newUser.set_password(data['newpassword'])
                newUser.save()
                return Response({'username': username, 'email': newUser.email, 'first_name': newUser.first_name, 'contact': newUser.last_name, 'id': newUser.id}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Username or Password are wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Bad Data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def AboutApi(request):
    try:
        # return specific data from database
        about = About.objects.get(id=1)
        serializer = AboutSerializer(about, many=False)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
