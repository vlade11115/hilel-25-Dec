# Generated by Django 4.2.6 on 2023-12-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_api", "0003_booktype_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
