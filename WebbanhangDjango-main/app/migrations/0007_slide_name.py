# Generated by Django 4.2.1 on 2023-05-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_slide_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]