
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ShippingAddressForm






# Create your views here.
def search(request):
 
    if request.method== "POST":
        seached = request.POST['searched']
        keys = Product.objects.filter(name__contains=seached)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item  
    else:
        # Tạo đối tượng order dựa trên session
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    slides = Slide.objects.all()

    return render(request, 'app/search.html', {'seached': seached, 'keys': keys,'products': products,'cartItems': cartItems, 'slides': slides,'categories': categories})

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        # print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
            show_error_dialog = True
    else:
        show_error_dialog = False
    context = {'show_error_dialog': show_error_dialog}
    return render(request, 'app/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item  
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Tạo đối tượng order dựa trên session
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"

    products = Product.objects.all()
    slides = Slide.objects.all()
    # categories = Category.objects.all()
    slides2 = Slide2.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    context= {'products': products,
              'slides': slides,
                'slides2': slides2,
                'cartItems': cartItems,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'categories': categories,
                'active_category': active_category,
              }
    
    return render(request, 'app/home.html',context)

def cart(request):
    # Xét xem người dùng đã đăng nhập hay chưa, nếu chưa thì chuyển hướng về trang đăng nhập, nếu đã đăng nhập thì lấy hoặc tạo đối tượng order dựa trên khách hàng, 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Tạo đối tượng order dựa trên session
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    slides = Slide.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    context= {'items': items, 
              'order': order,
              'cartItems': cartItems,
              'user_not_login': user_not_login,
              'user_login': user_login,
              'categories': categories,
              'active_category': active_category,
              'slides': slides,
       
              }
    return render(request, 'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"

    slides = Slide.objects.all()
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = request.user
            shipping_address.order = order
            shipping_address.save()
            if form.cleaned_data['save_info']:
                request.user.save_info = True
                request.user.save()


            order.complete = True
            order.save()

            return redirect('order_complete')
    else:
        form = ShippingAddressForm()

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'categories': categories,
        'active_category': active_category,
        'slides': slides,
        'form': form,  # Thêm form vào context để hiển thị trong template
    }
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    # quantity= data['quantity']
    action = data['action']
    print('Action:',action)
    print('productId:',productId)
    # print('quantity:',quantity)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # Tạo đối tượng orderitem
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
   
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    # Lưu lại số lượng sản phẩm
    orderItem.save()
    # Nếu số lượng sản phẩm bằng 0 thì xóa sản phẩm khỏi order
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def category(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Tạo đối tượng order dựa trên session
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    slides = Slide.objects.all()
    context = {'categories': categories,'products': products,'active_category': active_category,'slides': slides,'cartItems': cartItems,'user_not_login': user_not_login,'user_login': user_login,}
    return render(request, 'app/category.html',context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Tạo đối tượng order dựa trên session
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','') 
    products = Product.objects.filter(id=id)
    products2 = Product.objects.get(id=id)
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    similar_products = Product.objects.filter(category__in=products2.category.all()).exclude(id=id)[:4]
    context= {'items': items, 'order': order,'cartItems': cartItems,'user_not_login': user_not_login,'user_login': user_login,'categories': categories,'active_category': active_category,'products': products,'similar_products': similar_products,}
    return render(request, 'app/detail.html',context)

def order_complete(request):
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(order__customer=request.user, order__complete=True).latest('date')
        order = Order.objects.filter(customer=request.user, complete=True).latest('date')
        items = order.orderitem_set.all()

    slides = Slide.objects.all()
    categories = Category.objects.filter(is_sub=False)
    context = {
            'shipping_address': shipping_address,
            'order': order,
            'items': items,
            'categories': categories,
            'slides': slides,
            
        }
    return render(request, 'app/order_complete.html', context)

