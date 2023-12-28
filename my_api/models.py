from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class BookType(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Book(models.Model):
    type = models.ForeignKey(BookType, on_delete=models.CASCADE)
    owner = models.ForeignKey("auth.User", related_name="books", on_delete=models.CASCADE, null=True)


class OrderQuantity(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class Order(models.Model):
    books = models.ManyToManyField(OrderQuantity)
    buyer = models.ForeignKey("auth.User", related_name="orders", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, null=True)
    invoice_url = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)


class MonoSettings(models.Model):
    public_key = models.CharField(max_length=100, unique=True)
    received_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_new(cls, get_monobank_public_key_callback):
        return cls.objects.create(public_key=get_monobank_public_key_callback())

    @classmethod
    def get_latest_or_add(cls, get_monobank_public_key_callback):
        latest = cls.objects.order_by("-received_at").first()
        if not latest:
            latest = cls.create_new(get_monobank_public_key_callback)
        return latest
