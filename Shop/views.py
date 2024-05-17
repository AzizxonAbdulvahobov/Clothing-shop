from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AbstractBaseUser 
from .utils import CartAuthenTicatedUser
from django.contrib.auth import authenticate, login, logout
from . import models 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from OnlineShop import settings
import stripe
from django.urls import reverse

# Create your views here.

def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'products':products,
    }
    return render(request, 'index.html', context)



@login_required
def index2(request):  
    if not request.user.is_authenticated:
        return redirect('log_in')
    categories = models.Category.objects.all()
    products = models.Product.objects.all().order_by('-id')
    cart_info = CartAuthenTicatedUser(request).get_cart_info()
    context = {
        'categories':categories,
        'products':products,
        'cart_total_quantity':cart_info['cart_total_quantity']
    }
    return render(request, 'index2.html', context)


def shop(request):
    categories = models.Category.objects.all()
    cart_info = CartAuthenTicatedUser(request).get_cart_info()
    context = {
        'categories':categories,
        'cart_total_quantity':cart_info['cart_total_quantity']
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
            return redirect('index2')
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
    comments = models.Comment.objects.filter(product=product)
    cart_info = CartAuthenTicatedUser(request).get_cart_info()
    context = {
        'product':product,
        'categories':categories,
        'products':products,
        'comments':comments,
        'cart_total_quantity':cart_info['cart_total_quantity']
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message') 
        models.Comment.objects.create(
            name=name,
            email=email,
            message=message,
            product=product,
            user=request.user,
        )
        return redirect('detail', product_id=product_id)

    return render(request, 'detail.html', context)



def category_detail(request, category):
    categories = models.Category.objects.all()
    products = models.Product.objects.filter(category_id = category) 
    cart_info = CartAuthenTicatedUser(request).get_cart_info()

    context = {
        'categories':categories,
        'products':products,
        'cart_total_quantity':cart_info['cart_total_quantity']
    }
    return render(request, 'category_detail.html', context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartAuthenTicatedUser(request, product_id, action)
        current_page = request.META.get('HTTP_REFERER', 'index')
        return redirect(current_page)
    return HttpResponse('Iltimos avval royhatdan o`ting')





def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenTicatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online Shop mahsulotlari'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request):
    return render(request, 'fath/success.html')




def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenTicatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online Shop mahsulotlari'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request):
    return render(request, 'success.html')


