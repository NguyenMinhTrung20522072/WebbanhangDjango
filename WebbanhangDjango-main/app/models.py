from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


# Create your models here.
#change forms register django
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
    def __init__(self, *args, **kwargs):
         super(CreateUserForm,self).__init__(*args, **kwargs)
         self.fields['username'].widget.attrs['class'] = 'form-control'
         self.fields['password1'].widget.attrs['class'] = 'form-control'
         self.fields['password2'].widget.attrs['class'] = 'form-control'

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', blank=True, null=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.name
   
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='product', blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    description = models.TextField(max_length=500, null=True, blank=True)
    description2 = models.TextField(max_length=1500, null=True, blank=True)
    description3 = models.TextField(max_length=1500, null=True, blank=True)
    description4 = models.TextField(max_length=1500, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    made = models.CharField(max_length=50, null=True, blank=True)
    effect = models.CharField(max_length=50, null=True, blank=True)
    features = models.CharField(max_length=1500, null=True, blank=True)

    def get_features_list(self):
        if self.features:
            return self.features.split(',')
        else:
            return []


    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS_CHOICES = (
        ('Chưa giao', 'Chưa giao'),
        ('Đã giao', 'Đã giao'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Chưa giao')

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
    street_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, null=True,blank=True)
    save_info = models.BooleanField(default=False)  # Thêm trường save_info
    


    def __str__(self):
        return self.street_address
    
class Slide(models.Model):
    name = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='banner/')
    caption = models.CharField(max_length=100)
    # Thêm các trường khác nếu cần thiết
    def __str__(self):
        return self.name

class Slide2(models.Model):
    name = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='banner/')
    caption = models.CharField(max_length=100)
    # Thêm các trường khác nếu cần thiết
    def __str__(self):
        return self.name
    


