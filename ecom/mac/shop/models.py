from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300000)
    pub_date=models.DateField()
    image=models.ImageField(upload_to='shop/images',default="")
    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    add_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=400)
    city=models.CharField( max_length=50)
    zip=models.IntegerField()
    state=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    def __str__(self):
        return self.name
    

# class cart(models.Model):
#     cart_json=models.CharField(max_length=5000)
#     user=models.CharField(max_length=40)

class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    phone=models.CharField(max_length=10,default=0)
    email=models.CharField(max_length=1111)
    address=models.CharField(max_length=1111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip=models.CharField(max_length=111)
    def __str__(self):
        return self.name

class UpdateOrders(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=1000)
    timestamp=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:7]+"..."
    
class categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    image=models.ImageField(upload_to='shop/images',default="")
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name