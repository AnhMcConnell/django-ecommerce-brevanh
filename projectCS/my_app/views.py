from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import datetime

from .utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def index(request):
    data = cartData(request)
    cartProducts = data['cartProducts']

    items = Item.objects.all()
    context = {'items': items, 'cartProducts': cartProducts}
    return render(request, 'my_app/index.html', context)


def shop(request):
    data = cartData(request)
    cartProducts = data['cartProducts']

    items = Item.objects.all()
    context = {'items': items, 'cartProducts': cartProducts}
    return render(request, 'my_app/shop.html', context)


def cart(request):
    data = cartData(request)
    cartProducts = data['cartProducts']
    order = data['order']
    products = data['products']

    context = {'products': products,'order': order,'cartProducts': cartProducts, 'shipping':False}
    return render(request, 'my_app/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartProducts = data['cartProducts']
    order = data['order']
    products = data['products']

    context = {'products': products,'order': order,'cartProducts': cartProducts, 'shipping': False}
    return render(request, 'my_app/checkout.html', context)

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action:', action)
    print('itemId:', itemId)

    customer = request.user.customer
    item = Item.objects.get(id=itemId)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = OrderItem.objects.get_or_create(order=order,item=item)

    if action == "add":
        orderItem.quantity = (orderItem.quantity +1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],)
    print('Data:', data)
    return JsonResponse('Payment Completed!', safe=False)
