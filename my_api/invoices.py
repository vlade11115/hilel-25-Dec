import requests
from django.conf import settings

from my_api.models import Order


def create_invoice(order: Order, webhook_url):
    amount = 0
    basket_order = []
    for order_quantity in order.books.all():
        sum_ = order_quantity.book.type.price * order_quantity.quantity
        amount += sum_
        basket_order.append(
            {"name": order_quantity.book.type.title, "qty": order_quantity.quantity, "sum": sum_, "unit": "шт."}
        )
    merchants_info = {"reference": str(order.id), "destination": "Купівля книжок", "basketOrder": basket_order}
    request_body = {"webHookUrl": webhook_url, "amount": amount, "merchantPaymInfo": merchants_info}
    headers = {"X-Token": settings.MONOBANK_TOKEN}
    r = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=request_body, headers=headers)
    r.raise_for_status()
    order.order_id = r.json()["invoiceId"]
    order.invoice_url = r.json()["pageUrl"]
    order.save()
