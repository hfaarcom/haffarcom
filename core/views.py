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
from datetime import date, timedelta, datetime
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
        print(data)
        if {'user', 'category', 'fields', 'subcategory', 'photosNum'} <= set(data):
            # check POST data
            about = About.objects.get(id=1)
            token = getToken(data['user'])
            user = User.objects.get(id=token.get('user_id'))
            category = Category.objects.get(id=data['category'])
            fields = data['fields']
            photosNum = data['photosNum']
            subcategory = SubCategory.objects.get(id=data['subcategory'])
            expire_date = date.today() + timedelta(days=About.objects.get(id=1).product_expire_days)
            if about.auto_approve == True:
                Pstatus = 'approved'
            elif about.auto_approve == False:
                Pstatus = 'pending'

            # convert STR to DICT/JSON
            Jfields = json.loads(fields)

            photosDict = {}
            errorPhotos = {}

            if Jfields.keys() == category.fields.keys():

                about.products_num += 1
                about.save()

                prodctId = GenerateUUID()
                if photosNum != 0:
                    for i in range(int(photosNum)):
                        requestPhotoName = f'photo-{i}'
                        if requestPhotoName in data:

                            uploadingName = f'{prodctId}-{i}'

                            check = checkFile(uploadingName)
                            if check:
                                url = uploadfile(
                                    request.data[requestPhotoName], uploadingName, 'png')
                                photosDict[requestPhotoName] = url
                            else:
                                errorPhotos[requestPhotoName] = 'File With That Name Exists'
                        else:
                            pass

            # check Product Fields

                # create New Product
                newProduct = Product.objects.create(
                    user=user,
                    category=category,
                    fields=Jfields,
                    status=Pstatus,
                    expire_date=expire_date,
                    subCategory=subcategory,
                    photos=photosDict,
                    uudi=prodctId,
                    views=0
                )

                Notification.objects.create(
                    user=user,
                    body='???? ?????????? ?????????? ??????????!'
                )

                # serialize data
                serializer = ProductsSerilizer(newProduct, many=False)

                # return data
                return Response({'data': serializer.data, 'errorPhotos': errorPhotos}, status=status.HTTP_201_CREATED)

            else:

                return Response({'error': 'Product Fields Does not match with its category'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT', 'DELETE'])
# def updateProductPhotos(request):
#     try:
#         data = request.data
#         print(data)
#         if {'product', 'photosNum'} <= set(data):
#             photosNum = data['photosNum']
#             product = Product.objects.get(id=data['product'])
#             errorPhotos = {}
#             if request.method == 'PUT':

#                 if photosNum != 0:
#                     productPhotosNum = len(product.photos)
#                     data.pop('photosNum')
#                     data.pop('product')
#                     data.pop('category')
#                     data.pop('subcategory')
#                     data.pop('fields')
#                     data.pop('user')
#                     data.pop('api_key')
#                     photosDict = {}
#                     for k, v in data.items():
#                         uploadingName = f'{product.uudi}-{productPhotosNum + 1}'
#                         check = checkFile(uploadingName)
#                         if check:
#                             url = uploadfile(
#                                 request.data[k], uploadingName, 'png')
#                             photosDict[k + uploadingName] = url
#                         else:
#                             errorPhotos[k] = 'File With That Name Exists'
#                     print('photos Before = ', product.photos)
#                     print('photosDict = ', photosDict)
#                     dest = {}
#                     dest.update(product.photos)
#                     dest.update(photosDict)
#                     print('dest = ', dest)
#                     product.photos = dest
#                     product.save()
#                     print('photos after = ', product.photos)

#                 return Response({'putPhotos': photosDict, 'errorPhotos': errorPhotos},  status=status.HTTP_200_OK)

#             elif request.method == 'DELETE':
#                 deletedPhotos = []
#                 for i in range(int(data['photosNum'])):
#                     photo = data[f'photo-{i}']
#                     photoName = photo.rsplit('/', 1)[1]
#                     check = checkFile(photoName)
#                     if not check:
#                         d = deleteFile(photoName)
#                         if d:
#                             product.photos.pop(f'photo-{i}')
#                             product.save()
#                             deletedPhotos.append(i)
#                         else:
#                             errorPhotos[i] = 'server error'
#                     else:
#                         errorPhotos[i] = 'photo doesnt exists'
#                 return Response({'deletedPhotos': deletedPhotos, 'errorPhotos': errorPhotos}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'bad data'}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProductByCat(request):
    try:
        data = request.query_params
        if 'category' in data:
            # check data + serialize it
            category = Category.objects.get(id=data['category'])
            products = Product.objects.filter(
                category=category, status='approved')

            serializer = ProductsSerilizer(products, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                subCategory=category, status='approved')

            serializer = ProductsSerilizer(products, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProductbyId(request):
    try:
        data = request.query_params
        if 'id' in data:
            # check data + serialize it
            product = Product.objects.get(id=data['id'])
            date = datetime.strptime(str(product.expire_date), '%Y-%m-%d')
            if datetime.today() > date:
                product.status = 'pending'
            product.views += 1
            product.save()
            serializer = ProductsSerilizer(product, many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllProducts(request):
    try:
        products = Product.objects.filter(status='approved').order_by('-id')
        serializer = ProductsSerilizer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def Productcomment(request):
    try:
        data = request.data
        if request.method == 'PUT':
            if {'token', 'description', 'product'} <= set(data):
                # check data + serialize it
                token = getToken(data['token'])
                user = User.objects.get(id=token['user_id'])
                product = Product.objects.get(id=data['product'])
                description = data['description']

                comment = Comment.objects.create(
                    user=user, product=product, description=description)

                serializer = CommentSerializer(comment, many=False)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if 'comment' in data:
                comment = Comment.objects.get(id=data['comment'])
                comment.delete()
                return Response({'deleted'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def CommentReplayView(request):
    try:
        data = request.data
        if request.method == 'PUT':
            if {'user', 'product', 'comment', 'description'} <= set(data):
                token = getToken(data['user'])
                user = User.objects.get(id=token['user_id'])
                product = Product.objects.get(id=data['product'])
                comment = Comment.objects.get(id=data['comment'])

                replay = CommentReplay.objects.create(
                    user=user,
                    product=product,
                    description=data['description']
                )
                comment.replaies.add(replay)
                comment.save()
                serializer = CommentSerializer(comment, many=False)

                return Response(serializer.data)

        elif request.method == 'DELETE':
            if {'replay'} <= set(data):
                replay = CommentReplay.objects.get(id=data['replay'])
                replay.delete()
                return Response({'deleted'})
    except Exception as e:
        return Response({'error': str(e)})

# ADS


@api_view(['GET'])
def ADS(request):
    try:
        # check data + serialize it
        ads = AD.objects.filter(status='approved')
        serializer = ADSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
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
                    return Response({'error': 'username or password are wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'username doesnt exsits'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateUser(request):
    try:
        data = request.data
        if {'contact', 'name', 'user'} <= set(data):
            if 'email' in data:
                email = data['email']
            else:
                email = ''
            contact = data['contact']
            first_name = data['name']
            token = getToken(data['user'])

            if User.objects.filter(id=token['user_id']).exists():
                user = User.objects.get(id=token['user_id'])
                user.email = email
                user.last_name = contact
                user.first_name = first_name
                user.save()

                return Response({'username': user.username, 'email': user.email, 'first_name': first_name, 'contact': contact, 'id': token['user_id'], 'token': get_tokens_for_user(user)}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': '???????????????? ?????? ??????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def Register(request):
    try:
        data = request.data
        print(data)
        print(request.query_params)
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
                return Response({'error': '?????? ???????????????? ?????? ??????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({'error': '?????? ???????????????? ???? ?????????? ?????????? ??????????'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserDetails(request):
    try:
        data = request.query_params
        print(data['token'])
#         if 'token' in data:
        token = getToken(data['token'])
        user = User.objects.get(id=token['user_id'])
        return Response({'username': user.username, 'name': user.first_name, 'contact': user.last_name, 'user': user.id, 'token': get_tokens_for_user(user), 'email': user.email}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUserDetailsById(request):
    try:
        data = request.query_params
        if 'id' in data:
            user = User.objects.get(id=data['id'])
            product = Product.objects.filter(user=user, status='approved')
            print(product)
            serializer = ProductsSerilizer(product, many=True)
            return Response({'user': {'username': user.username, 'name': user.first_name, 'contact': user.last_name, 'user': user.id, 'token': get_tokens_for_user(user), 'email': user.email},
                             'products': serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['GET', 'POST', 'DELETE'])
def UserNotifications(request):
    try:
        if request.method == 'GET':
            data = request.query_params
            if 'user' in data:
                token = getToken(data['user'])
                user = User.objects.get(id=token['user_id'])
                noti = Notification.objects.filter(user=user)
                serializer = NotificationSerializer(noti, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            data = request.data
            if 'id' in data:
                noti = Notification.objects.get(id=data['id'])
                noti.delete()
                return Response({'deleted'})
            elif 'user' in data:
                token = getToken(data['user'])
                user = User.objects.get(id=token['user_id'])
                noti = Notification.objects.filter(user=user)
                noti.delete()
                return Response({'cleared'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'POST':
            data = request.data
            if {'user', 'body'} <= set(data):
                token = getToken(data['user'])
                user = User.objects.get(id=token['user_id'])
                body = data['body']

                noti = Notification.objects.create(
                    user=user,
                    body=body
                )

                serializer = NotificationSerializer(noti, many=False)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': '?????? ???? ??????????????! ???????? ?????????????? ???? ?????????? ???????????????? ????????????????'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
