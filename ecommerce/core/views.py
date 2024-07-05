from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Evento
from django.db.models import Sum

from item.models import Category, Item

from .forms import SignupForm, SquadraForm, AzioneForm
from .models import Order, Address, Squadra, Azione, SquadraAzione


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {'categories': categories, 'items': items})


def contact(request):
    return render(request, 'core/contact.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            shipping_address = form.cleaned_data.get('shipping_address')
            billing_address = form.cleaned_data.get('billing_address')
            Address.objects.create(user=user, shipping_address=shipping_address, billing_address=billing_address)

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def cart_view(request):
    cart_items = request.session.get('cart', [])
    items = Item.objects.filter(id__in=cart_items)
    total_price = sum(item.price for item in items)

    item_quantities = {}
    if request.method == 'POST':
        item_quantities = {str(item.id): request.POST.get(str(item.id), '1') for item in items}

    return render(request, 'core/cart.html',
                  {'items': items, 'total_price': total_price, 'item_quantities': item_quantities})


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

    items = Item.objects.filter(id__in=cart_items)
    total_price = sum(item.price * cart_items.count(item.id) for item in items)

    return render(request, 'core/cart.html', {'items': items, 'total_price': total_price})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})


def create_order(request):
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        order = Order.objects.create(user=request.user, status='processing')
        order.items.add(*cart_items)
        del request.session['cart']
        return redirect('core:place_order')
    else:
        return redirect('core:cart')


@login_required
def order_summary(request):
    allowed_statuses = ['processing']

    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    if request.method == 'POST' and request.user.is_superuser:
        order_id = request.POST.get('order_id')
        shipping_status = request.POST.get('shipping_status')
        order = get_object_or_404(Order, id=order_id)
        order.shipping_status = shipping_status
        order.save()
        return redirect('core:order_summary')

    for order in orders:
        order.total_price = sum(item.price for item in order.items.all())
        order.save()

    return render(request, 'core/order_summary.html', {'orders': orders, 'allowed_statuses': allowed_statuses})


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == 'POST' and order.status in ['pending_payment', 'processing']:
        order.delete()

    return redirect('core:order_summary')


def place_order(request):
    payment_data = request.POST.get('payment_data', None)
    if payment_data:
        return redirect('payment_confirmation')
    return render(request, 'core/payment_confirmation.html', {'error_message': 'Dati di pagamento non validi'})


@login_required
def update_shipping_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        shipping_status = request.POST.get('shipping_status')

        order = get_object_or_404(Order, id=order_id)
        order.shipping_status = shipping_status
        order.save()

    return redirect('core:order_summary')

def fantamatrimonio(request):
    if request.method == 'POST':
        squadra_form = SquadraForm(request.POST)
        azione_form = AzioneForm(request.POST)

        if squadra_form.is_valid() and azione_form.is_valid():
            squadra = squadra_form.save()

            # Salva l'azione esclusiva
            azione_esclusiva = azione_form.cleaned_data['azioni_esclusive']
            SquadraAzione.objects.create(squadra=squadra, azione=azione_esclusiva, completata=True)

            # Salva le azioni non esclusive
            for azione in azione_form.cleaned_data['azioni']:
                SquadraAzione.objects.create(squadra=squadra, azione=azione, completata=True)

            return redirect('core:classifica')

    else:
        squadra_form = SquadraForm()
        azione_form = AzioneForm()

    context = {
        'squadra_form': squadra_form,
        'azione_form': azione_form
    }
    return render(request, 'core/fantamatrimonio.html', context)

def classifica(request):
    squadre = Squadra.objects.all().annotate(total_points=Sum('squadraazione__azione__punti')).order_by('-total_points')
    context = {'squadre': squadre}
    return render(request, 'core/classifica.html', context)