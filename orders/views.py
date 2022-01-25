from django.shortcuts import redirect, render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse

# Create your views here.
def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    form = OrderCreateForm(request.POST)
    if form.is_valid():
      order = form.save()
      for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
      cart.clear()
      # return render(request, 'orders/order/created.html', {'order': order})
      # set the order in the session
      request.session['order_id'] = order.id
      # redirect for payment
      return redirect(reverse('payment:process'))
  else:
    form = OrderCreateForm()
  return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})