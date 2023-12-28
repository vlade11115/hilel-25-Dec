from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from my_api.models import Author, Book, Order, BookType, OrderQuantity
from .invoices import create_invoice, verify_signature
from .permissions import IsOwnerOrReadOnly
from .serializers import AuthorSerializer, BookSerializer, OrderSerializer, BookTypeSerializer, OrderInputSerializer


class AuthorsList(generics.ListCreateAPIView, GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorsDetail(generics.RetrieveUpdateDestroyAPIView, GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BookTypeViewSet(viewsets.ModelViewSet):
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer


class OrderViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.DestroyAPIView, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        order = Order()
        order.buyer = request.user
        order.save()
        s = OrderInputSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        for order_item in s.validated_data["order"]:
            order_item["book"] = Book.objects.get(id=order_item["book"])
            q = OrderQuantity.objects.create(book=order_item["book"], quantity=order_item["quantity"])
            order.books.add(q)
        order.save()
        create_invoice(order, reverse("webhook-mono", request=request))
        # create_invoice(order, "https://webhook.site/9dee6af0-a1ea-4bfb-81fe-6e42a50775d4")
        return Response({"invoice_url": order.invoice_url})


class MonoAcquiringWebhookReceiver(APIView):
    def post(self, request):
        try:
            verify_signature(request)
        except Exception:
            return Response({"status": "error"}, status=400)
        reference = request.data.get("reference")
        order = Order.objects.get(id=reference)
        if order.order_id != request.data.get("invoiceId"):
            return Response({"status": "error"}, status=400)
        order.status = request.data.get("status", "error")
        order.save()
        return Response({"status": "ok"})
