import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    products = []
    order = {'get_cart_total':0, 'get_cart_items': 0}
    cartProducts = order['get_cart_items']

    for i in cart:
        try:
            cartProducts += cart[i]["quantity"]

            item = Item.objects.get(id=i)
            total = (item.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            product = {
                'item' :{
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'imageURL': item.imageURL,
                    },
                'quantity': cart[i]["quantity"],
                'get_total': total
                }
            products.append(product)
            order['shipping'] = True
        except:
            pass
    return {'cartProducts': cartProducts, 'order': order, 'products':products}

def cartData(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        products = order.orderitem_set.all()
        cartProducts = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartProducts = cookieData['cartProducts']
        order = cookieData['order']
        products = cookieData['products']
    return {'cartProducts': cartProducts, 'order': order, 'products':products}

def guestOrder(request, data):
    print("User is not logged in!")
    print("COOKIES:", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    products = cookieData['products']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for product in products:
        item = Item.objects.get(id=product['item']['id'])
        orderProduct = OrderItem.objects.create(
            item=item,
            order=order,
            quantity=product['quantity']
        )

    return customer, order
