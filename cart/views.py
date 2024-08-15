from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from events.models import Event
from .cart import Cart
from .forms import CartAddEventForm

@require_POST
def cart_add(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    form = CartAddEventForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            event=event,
            quantity=[cd['quantity']],
            override_quantity=cd['override'],
        )
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    cart.remove(event)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})