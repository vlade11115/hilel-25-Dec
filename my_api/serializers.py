from rest_framework import serializers

from .models import Author, Book, Order, BookType


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "id"]


class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ["title", "author", "id"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["type", "id", "owner"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["books", "id"]


class OrderQuantitySerializer(serializers.Serializer):
    book = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderInputSerializer(serializers.Serializer):
    order = OrderQuantitySerializer(many=True)
