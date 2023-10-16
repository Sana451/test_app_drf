from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}"


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='accesses')
    is_valid = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='user_product_unique_constraint')
        ]

    def __str__(self):
        return f"{self.user.username} => {self.product} (is_valid={self.is_valid})"
