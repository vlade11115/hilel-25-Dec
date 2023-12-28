import base64
import hashlib

import ecdsa
import requests
from django.conf import settings

from my_api.models import Order

MONOBANK_PUBLIC_KEY = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFc05mWXpNR1hIM2VXVHkzWnFuVzVrM3luVG5CYgpnc3pXWnhkOStObEtveDUzbUZEVTJONmU0RlBaWmsvQmhqamgwdTljZjVFL3JQaU1EQnJpajJFR1h3PT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="


def verify_signature(request):
    # example pubkey, you should receive one at https://api.monobank.ua/api/merchant/pubkey
    # value from X-Sign header in webhook request
    x_sign_base64 = request.headers["X-Sign"]

    # webhook request body bytes
    body_bytes = request.body

    pub_key_bytes = base64.b64decode(MONOBANK_PUBLIC_KEY)
    signature_bytes = base64.b64decode(x_sign_base64)
    pub_key = ecdsa.VerifyingKey.from_pem(pub_key_bytes.decode())

    ok = pub_key.verify(signature_bytes, body_bytes, sigdecode=ecdsa.util.sigdecode_der, hashfunc=hashlib.sha256)
    if not ok:
        raise Exception("Signature is not valid")


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
