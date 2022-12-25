hello world!

let's start:

for use the api u need few things to understand first

1- the api key
some endpoints needs api_key to access to it

2- only allowed methods are POST, GET only

3- in this docs i'm gonna mention every end point + its details

4- in error case the returned data gonna be like:
{‘error’: Error Line}

5- data fields if u want u can check it :
```python
class Product(models.Model):
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=100, null=True, choices=PRODUCT_STATUS)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True)
    subCategory = models.ForeignKey(
        'SubCategory', on_delete=models.CASCADE, null=True)
    fields = models.JSONField()

class Category(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    photo = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        choices=CATEGORY_STATUS, null=True, blank=True, max_length=100, default='approved')
    fields = models.JSONField(null=True, default=get_default)

class SubCategory(models.Model):
    mainCategory = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    photo = models.CharField(max_length=1000, blank=True, null=True)

class AD(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=ADS_STATUS, null=True, blank=True, max_length=100)
    photo = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=100, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class About(models.Model):
    app_name = models.CharField(max_length=100, null=True)
    icon_link = models.CharField(max_length=1000, null=True)
    privacy_policy = models.CharField(max_length=100000, null=True)
    about_us = models.CharField(max_length=10000, null=True)
    contact_number = models.CharField(max_length=100, null=True)
    whatsup_number = models.CharField(max_length=100, null=True)
    agree_text = models.CharField(max_length=100000, null=True)
    payment_info_text = models.CharField(max_length=100000, null=True)
    payment_info_link = models.CharField(
        max_length=1000, null=True, blank=True)
    product_expire_days = models.IntegerField(null=True, blank=True)
```

its so easy to read
and u can check every table and its fields and data type
—--------------------------------

1- products endpoints:
-------------------------------
1- create new product:


	- method : POST
	
	- endpoint : /products/create/

	- data to post : 
	
	{
	
	- ‘user’: user id, Int
	
	- ‘category’ : category id, Int
	
	- ‘fields’ : product fields, Object
	
	- ‘subcategory’: subcategory id, Int
	
	- 'photos' : product photos, Object
	
	}

----------------------------------------
photos object have to be like this :
```
{
'image 1 name' : image,
'image 2 name' : image,
etc...
}
```
```
image name have to be :

1- unique name
2- the name have to contain the prodcut ID + the number of photo (start counting from 1 )
3- the name for the image it self doesnt matter, the important thing is the key in the dict
3- supported types are 1- PNG, 2-JPG

example:

'photos' : {
'productId-1.png': screensho1.png,
'productId-2.png': sfsdf.png,
'productId-3.png': sdffds.png,
}
```


----------------------------------------
product fields have to match its category fields

u can get product category fields by using category fields api 

----------------------------------------
```
category/subcategory/fields data depends on user choices
```

returned data : 

{

'data' : {

‘user’:user id,

category:category id,

fields: product fields, {
  # for example :
  'title': 'product 1',
  'price': '100',
  etc...
}

status: product status , by default its ‘approved’

expire_date: product expire date,

subcategory: subcategory id,

photos: {
'image 1 name' : 'image 1 url',
'image 2 name' : 'image 2 url'
etc....
}
},

}

http status : 201

possible errors:

{'error': 'Product Fields Does not match with its category'}
	in this case u have to check product fields keys that u post, it has to match the category fields keys that given

```python 
    fields = data[‘fields’]
    category = Category.objects.get(id=data[‘category’])
    # convert STR to DICT/JSON
    Jfields = json.loads(fields)
 
    # check Product Fields
    if Jfields.keys() == category.fields.keys():
	do some stuff
    else:
	return {{'error': 'Product Fields Does not match with its category'}}
```

—-
{'error': 'bad request'}

in this case check again the data that given : 
it has to be : 
```python
{'user', 'category', 'fields', 'subcategory'}
```
user id
category id
subcategory id
fields : object

—-


2- get user products
 method: GET,
endpoint : /product/get/user/,
required query params : 
{‘user’:’user id’, ‘status’:’product status’}

product status has to be one of these:
```
    ('approved),
    ('declined'),
    ('pending'),
    ('sold'),
    ('Deleted')
```
if u want to get all products with all status
set status to 'all'

```python
# get data + serialize it
if data['status'] != 'all':
  products = Product.objects.filter(
  user=data['user'], status=data['status'])
else:
  products = Product.objects.filter(user=data['user'])
```

returned data :
{
date: product created date,
user: user id,
expire_date : product expire date,
status: product status,
category: category id,
subcategory : subcategory id,
fields : product fields , OBJECT!
}

errors:
```
{'error': 'bad request'}
```

pls recheck the given data
it has to be :
```
 {'user', 'status'}
```

3- get products by specific category 
method : GET
endpoint : /product/get/category/
required query params:
{'category': category id}

returned data :
[
list with all products with that category
]

errors :
bad request
check query params 

4- get products by subcategory 
method : GET
endpoint : product/get/category/sub/
query params:
subcategory : subcategory id 

returned data : 
[
list with all products with that subcategory
]

errors:
bad request :
check query params

5- get product data by product id
method : GET

endpoint : /product/get/id/

query params:

id : product id

returned data:
{
product data here,
}

errors:
bad data
check query params

6- update product fields data
method : POST

endpoint : /product/update/fields/

data to post :

product : product id,

fields  : ALL product fields even the ones which u dont want to update

note :
* the new fields that u wanna update has to match with product category fields
or u gonna get this error: 
```
{'error': 'Product Fields Does not match with its category'}, status=status.HTTP_400_BAD_REQUEST}
```
returned data :
{
product with new fields data
}
