# Generated by Django 4.2.1 on 2023-05-31 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_product_description2'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description3',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
