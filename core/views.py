from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .utails import *
import json
from datetime import date, timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Products


@api_view(['POST'])
def addNewProduct(request):
    try:
        data = request.data
        if {'user', 'category', 'fields', 'subcategory', 'photos'} <= set(data):
            # check POST data
            token = getToken(data['user'])
            user = User.objects.get(id=token.get('user_id'))
            category = Category.objects.get(id=data['category'])
            fields = data['fields']
            photos = data['photos']
            subcategory = SubCategory.objects.get(id=data['subcategory'])
            expire_date = date.today() + timedelta(days=About.objects.get(id=1).product_expire_days)

            # convert STR to DICT/JSON
            Jfields = json.loads(fields)
            Jphotos = json.loads(photos)

            photosDict = {}
            errorPhotos = {}

            for k, v in Jphotos:
                check = checkFile(k)
                if check:
                    url = uploadfile(v.file, k, 'png')
                    photosDict[k] = url
                else:
                    errorPhotos[k] = 'File With That Name Exists'

            # check Product Fields
            if Jfields.keys() == category.fields.keys():

                # create New Product
                newProduct = Product.objects.create(
                    user=user,
                    category=category,
                    fields=Jfields,
                    status='approved',
                    expire_date=expire_date,
                    subCategory=subcategory,
                    photos=photosDict
                )

                # serialize data
                serializer = ProductsSerilizer(newProduct, many=False)

                # return data
                return Response({'data': serializer.data, 'errorPhotos': errorPhotos}, status=status.HTTP_201_CREATED)

            else:

                return Response({'error': 'Product Fields Does not match with its category'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateProductPhotos(request):
    try:
        data = request.data
        if {'product', 'photos'} <= set(data):
            photos = data['photos']
            product = Product.objects.get(id=data['product'])
            errorPhotos = {}
            if request.method == 'PUT':
                Jphotos = json.loads(photos)
                photosDict = {}

                for k, v in Jphotos:
                    check = checkFile(k)
                    if check:
                        url = uploadfile(v.file, k, 'png')
                        photosDict[k] = url
                    else:
                        errorPhotos[k] = 'File With That Name Exists'

                product.photos = photosDict
                product.save()

                return Response({'putPhotos': photosDict, 'errorPhotos': errorPhotos})

            elif request.method == 'DELETE':
                deletedPhotos = []
                for i in photos:
                    check = checkFile(i)

                    if not check:
                        d = deleteFile(i)
                        if d:
                            product.photos.pop(i)
                            product.save()
                            deletedPhotos.append(i)
                        else:
                            errorPhotos[i] = 'server error'
                    else:
                        errorPhotos[i] = 'photo doesnt exists'
                return Response({'deletedPhotos': deletedPhotos, 'errorPhotos': errorPhotos}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserProducts(request):
    try:
        data = request.query_params
        if {'user', 'status'} <= set(data):
            token = getToken(data['user'])
            # get data + serialize it
            if data['status'] != 'all':
                products = Product.objects.filter(
                    user=token['user_id'], status=data['status'])
            else:
                products = Product.objects.filter(user=token['user_id'])

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
            category = Category.objects.get(id=data['category'])
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
            category = SubCategory.objects.get(id=data['subcategory'])
            products = Product.objects.filter(
                subCategory=category)

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
            return Response({'error': 'Bad Data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateProdcutFields(request):
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


@api_view(['POST'])
def updateProductStatus(request):
    try:
        data = request.data
        if {'status', 'product'} <= set(data):
            product = Product.objects.get(id=data['product'])
            product.status = data['status']
            product.save()
            return Response({'updated': product.status}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateProductExpireDate(request):
    try:
        data = request.data
        if {'product'} <= set(data):
            product = Product.objects.get(id=data['product'])
            product.expire_date = date.today(
            ) + timedelta(days=About.objects.get(id=1).product_expire_days)
            product.save()
            return Response({'updated': product.expire_date}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
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
                category = Category.objects.filter(status='approved')
                serializer = CategorySerializer(category, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Bad API_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'API_KEY required'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCategory(request):
    try:
        data = request.query_params
        if {'api_key', 'category'} <= set(data):
            if data['api_key'] == settings.API_KEY:
                # check data + serialize it
                category = Category.objects.get(id=data['category'])
                serializer = CategorySerializer(category, many=False)
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
def Productcomment(request):
    try:
        data = request.data
        if request.method == 'PUT':
            if {'user', 'description', 'product'} <= set(data):
                # check data + serialize it
                user = User.objects.get(id=data['user'])
                product = Product.objects.get(id=data['product'])
                description = data['description']

                comment = Comment.objects.create(
                    user=user, product=product, description=description)

                serializer = CommentSerializer(comment, many=False)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if 'comment' in data:
                comment = Comment.objects.get(id=data['comment'])
                comment.delete()
                return Response({'deleted'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ADS


@api_view(['GET'])
def ADS(request):
    try:
        data = request.query_params
        if 'api_key' in data:
            if data['api_key'] == settings.API_KEY:
                # check data + serialize it
                ads = AD.objects.all()
                serializer = ADSerializer(ads, many=True)
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
        if {'username', 'password'} <= set(data):
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
                    token = get_tokens_for_user(user)
                    return Response({'user': user.id, 'username': user.username, 'name': user.first_name, 'contact': user.last_name, 'email': user.email, 'token': token}, status=status.HTTP_202_ACCEPTED)
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
            token = getToken(data['user'])

            if User.objects.filter(id=token['user_id']).exists():
                user = User.objects.get(id=token['user_id'])
                user.email = email
                user.last_name = contact
                user.first_name = first_name

                user.save()

                return Response({'username': user.username, 'email': email, 'first_name': first_name, 'contact': contact, 'id': token['user_id'], 'token': token}, status=status.HTTP_201_CREATED)
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
        if {'username', 'password', 'name', 'contact'} <= set(data):
            # check data + serialize it
            username = data['username']
            first_name = data['name']
            contact = data['contact']
            # check if username and email are unique
            if not User.objects.filter(username=username).exists():
                newUser = User.objects.create_user(
                    username=username, password=data['password'])
                newUser.first_name = first_name
                # Last Name is the contact Number ...
                newUser.last_name = contact
                newUser.save()
                token = get_tokens_for_user(newUser)
                return Response({'username': username, 'name': first_name, 'contact': contact, 'user': newUser.id, 'token': token}, status=status.HTTP_201_CREATED)
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
                token = get_tokens_for_user(newUser)
                return Response({'username': username, 'name': newUser.first_name, 'contact': newUser.last_name, 'user': newUser.id, 'token': token}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Username or Password are wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Bad Data'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserDetails(request):
    try:
        data = request.query_params
        if 'token' in data:
            token = getToken(data['token'])
            user = User.objects.get(user=token['user_id'])
            return Response({'username': user.username, 'name': user.first_name, 'contact': user.last_name, 'user': user.id, 'token': token}, status=status.HTTP_202_ACCEPTED)
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
