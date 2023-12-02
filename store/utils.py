from .models import Product, Order,OrderItem, Customer
import json


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for key in cart:
        try:
            cart_items += cart[key]['quantity']

            product = Product.objects.get(id=key)
            total = (product.price * cart[key]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[key]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[key]['quantity'],
                'get_total': total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cart_items': cart_items, 'order': order, 'items': items}


def get_cart_data(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']
    return {'cart_items': cart_items, 'order': order, 'items': items}


def geust_order(request, data):
    name = data['form']['name']
    email = data['form']['email']
    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product, order=order, quantity=item['quantity'])

    return customer, order