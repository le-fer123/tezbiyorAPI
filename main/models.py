from django.db import models, transaction

class User(models.Model):
    tg_id = models.IntegerField(primary_key=True, verbose_name='Telegram ID', unique=True, blank=False, null=False, default=None)
    fullname = models.CharField(max_length=255, blank=False, null=True)
    phone_number = models.CharField(max_length=255, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, null=True)
    desc = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='category/', blank=False, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128, blank=False, null=True)
    desc = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=False, null=True)
    img = models.ImageField(upload_to='product/', blank=False, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=False, null=True)
    shipping_address = models.CharField(max_length=128, blank=False, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    status = models.CharField(max_length=128, blank=False, null=True)
    desc = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def update_total_price(self):
        with transaction.atomic():
            print(self.order_items.all())
            self.total_price = sum(item.price for item in self.order_items.all())
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', blank=False, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    quantity = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return str(self.id)