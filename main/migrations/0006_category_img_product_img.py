# Generated by Django 5.0.7 on 2024-08-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_user_id_order_user_alter_order_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(null=True, upload_to='category/'),
        ),
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(null=True, upload_to='product/'),
        ),
    ]
