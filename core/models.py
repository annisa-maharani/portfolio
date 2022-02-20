from django.db import models
from django.contrib.auth.models import User


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey('backend.ProductReview', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.p_title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    item = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('beauty.Address', on_delete=models.SET_NULL, null=True, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for item in self.item.all():
            total += item.get_final_price()
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    disc_amount = models.IntegerField(default=10_000, verbose_name='Besar Potongan Harga : ')

    def __str__(self):
        return self.code
