from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Order, Cart, CartItem
from .forms import UserRegisterForm, OrderForm
from django.db.models import Q

from .forms import UserRegisterForm, OrderForm, ProfileForm
from .models import Profile, Product

from .models import Product

def home(request):
    featured_products = Product.objects.all()[:3]
    return render(request, 'store/home.html', {'featured_products': featured_products})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def product_list(request):
    coffee_type = request.GET.get('coffee_type')
    if coffee_type:
        products = Product.objects.filter(coffee_type=coffee_type)
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.is_ordered = True
            order.save()
            send_mail(
                'Order Confirmation',
                f'Thank you for your order of {product.name}.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            messages.success(request, 'Order placed successfully!')
            return redirect('product_list')
    else:
        form = OrderForm(initial={'product': product})
    return render(request, 'store/place_order.html', {'form': form, 'product': product})

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []
    return render(request, 'store/search_results.html', {'products': products, 'query': query})

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

from .forms import UserRegisterForm, OrderForm, ProfileForm
from .models import Profile

@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'store/profile.html', {'form': form})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    return render(request, 'store/cart.html', {'cart': cart, 'items': items})

from django.shortcuts import redirect

from django.http import JsonResponse

@login_required
@require_POST
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    count = cart.items.count()
    return JsonResponse({'success': True, 'message': f'Added {product.name} to cart.', 'count': count})

@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': 'Item removed from cart.'})

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.items.count()
    else:
        count = 0
    return JsonResponse({'count': count})
