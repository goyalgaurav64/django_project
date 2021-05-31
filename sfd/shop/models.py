from django.db import models

# Create your models here.
#it creates the table product with fields as prod_id,prod_name etc..
class Product(models.Model):   #see documentation
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=50)
    category=models.CharField(max_length=60,default="")
    subcategory=models.CharField(max_length=60,default="")
    price=models.FloatField(default=0)
    prod_Description=models.CharField(max_length=40000)
    tag1=models.CharField(max_length=100,default="")
    tag2=models.CharField(max_length=100,default="")
    tag3=models.CharField(max_length=100,default="")
    tag4=models.CharField(max_length=100,default="")
    tag5=models.CharField(max_length=100,default="")
    publish_date=models.DateField()
    prod_image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.prod_name

class Contact(models.Model):   #see documentation
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=70,default="")
    desc=models.CharField(max_length=1000,default="")



    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=10000)
    amount = models.IntegerField(default=0)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default='')
    update_desc=models.CharField(max_length=10000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:20]+"..."+"_ order ID "+str(self.order_id)


    # to test code in terminal or powershell
    # run command -> python manage.py shell
    # then do the testing by applying the following
    # to save the date import -> from django.utils import timezone
    # import -> from shop.models import Product
    # to save the new product
    # myProd=Product(prod_name="mouse",category="electronics",subcategory="devices",price="12")
    # myProd.save()
    # to access the detail -> myProd.prod_id
    # to show all the tables -> Product.objects.all()
    # to get particular product -> Product.objects.get(prod_name="mouse") 