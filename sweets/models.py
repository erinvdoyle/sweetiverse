from django.db import models
import uuid
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Type(models.Model):
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='types')

    def __str__(self):
        return self.friendly_name


class Sweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    ingredients = models.TextField()
    flavor = models.CharField(max_length=100)
    country_of_origin = CountryField()
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='sweets')
    stock_amount = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(default=0)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_sale_price(self):
        """Automatically calculate the sale price if there's a discount."""
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price

    def save(self, *args, **kwargs):
        """Override save to calculate sale price and update stock status."""
        self.sale_price = self.calculate_sale_price()
        self.in_stock = self.stock_amount > 0
        super().save(*args, **kwargs)

    def update_rating(self):
        """Recalculate average rating from all related reviews."""
        average = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if average is not None:
            self.rating = round(average, 1)
            self.save()

class SweetReview(models.Model):
    sweet = models.ForeignKey(Sweet, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sweet', 'user')

    def __str__(self):
        return f'Review for {self.sweet.name} by {self.user.username}'
