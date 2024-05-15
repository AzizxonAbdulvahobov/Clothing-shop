from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AbstractBaseUser 
from .utils import CartAuthenTicatedUser
from django.contrib.auth import authenticate, login, logout
from . import models 
from django.http import HttpResponse

# Create your views here.

def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'products':products
    }
    return render(request, 'index.html', context)



def shop(request):
    categories = models.Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'shop.html', context)


def cart(request):
    cart_info = CartAuthenTicatedUser(request).get_cart_info()
    context = {
        'order_products':cart_info['order_products'],
        'cart_total_price':cart_info['cart_total_price'],
        'cart_total_quantity':cart_info['cart_total_quantity']
    }
    return render(request, 'cart.html', context)

def checkout(request):
    return render(request, 'checkout.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password-confirm']
        if password==password_confirm:
            User.objects.create_user(
                username=username,
                password=password
            )
    return render(request, 'register.html')

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('register')

    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('index')



def detail(request, product_id):
    product = models.Product.objects.get(id=product_id)
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    comments = models.Comment.objects.all()
    context = {
        'product':product,
        'categories':categories,
        'products':products,
        'comments':comments
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message') 
        models.Comment.objects.create(
            name=name,
            email=email,
            message=message
        ) 

    return render(request, 'detail.html', context)



def category_detail(request, category):
    categories = models.Category.objects.all()
    products = models.Product.objects.filter(category_id = category) 
    context = {
        'categories':categories,
        'products':products
    }
    return render(request, 'category_detail.html', context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartAuthenTicatedUser(request, product_id, action)
        current_page = request.META.get('HTTP_REFERER', 'index')
        return redirect(current_page)
    return HttpResponse('Iltimos avval royhatdan o`ting')