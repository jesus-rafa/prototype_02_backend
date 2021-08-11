from .models import Order, OrderItem


def update_order(idOrder):
    amount = 0
    quantity = 0

    instance_order = Order.objects.get(
        pk=idOrder
    )
    # obtenemos cantidad y total
    cart = OrderItem.objects.filter(
        order=idOrder
    )
    for item in cart:
        quantity = quantity + item.quantity
        amount = amount + (item.quantity * item.price)

    # actualizamos cantidad y total
    instance_order.quantity = quantity
    instance_order.amount = amount
    instance_order.save()

    return True
