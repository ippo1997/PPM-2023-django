from django.shortcuts import render, redirect, get_object_or_404

from item.models import Category, Item

from .forms import SignupForm
from .models import Order


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {'categories': categories, 'items': items})


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def cart_view(request):
    cart_items = request.session.get('cart', [])
    items = Item.objects.filter(id__in=cart_items)
    total_price = sum(item.price for item in items)
    return render(request, 'core/cart.html', {'items': items, 'total_price': total_price})


def add_to_cart(request, item_id):
    cart_items = request.session.get('cart', [])
    cart_items.append(item_id)
    request.session['cart'] = cart_items
    return redirect('core:cart')


def remove_from_cart(request, item_id):
    cart_items = request.session.get('cart', [])
    if item_id in cart_items:
        cart_items.remove(item_id)
        request.session['cart'] = cart_items
    return redirect('core:cart')


def update_cart_item_quantity(request, item_id):
    cart_items = request.session.get('cart', [])
    quantity = int(request.POST.get('quantity', 1))
    if item_id in cart_items:
        cart_items.remove(item_id)
        cart_items += [item_id] * quantity
        request.session['cart'] = cart_items
    return redirect('core:cart')


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})


def create_order(request):
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        order = Order.objects.create(user=request.user, status='pending_payment')
        order.items.add(*cart_items)
        del request.session['cart']
        return redirect('core:order_detail', pk=order.pk)
    else:
        return redirect('core:cart')


