# Generated by Django 5.0.7 on 2024-08-10 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_user_groups_remove_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True)),
                ('desc', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.CharField(max_length=128, null=True)),
                ('total_price', models.FloatField(null=True)),
                ('status', models.CharField(max_length=128, null=True)),
                ('desc', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True)),
                ('desc', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='main.order')),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
    ]
