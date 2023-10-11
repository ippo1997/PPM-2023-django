from your_app.models import Order

# Recupera tutti gli ordini dal database
orders = Order.objects.all()

# Crea un dizionario per riepilogare gli ordini con gli oggetti acquistati
order_summary = {}

# Itera su ciascun ordine e riepilogalo con gli oggetti
for order in orders:
    order_id = order.id
    user = order.user.username
    status = order.status
    shipping_status = order.shipping_status
    total_price = order.total_price

    # Recupera gli oggetti associati a questo ordine
    items = [item.name for item in order.items.all()]

    # Crea una voce di riepilogo dell'ordine
    order_summary[order_id] = {
        'user': user,
        'status': status,
        'shipping_status': shipping_status,
        'total_price': total_price,
        'items': items,
    }

# Stampiamo il riepilogo degli ordini
for order_id, summary in order_summary.items():
    print(f'Order ID: {order_id}')
    print(f'User: {summary["user"]}')
    print(f'Status: {summary["status"]}')
    print(f'Shipping Status: {summary["shipping_status"]}')
    print(f'Total Price: {summary["total_price"]}')
    print(f'Items: {", ".join(summary["items"])}')
    print()

# Questo codice recupererà tutti gli ordini dal tuo database e creerà un riepilogo
# con gli oggetti associati a ciascun ordine. Successivamente, stampa il riepilogo.
