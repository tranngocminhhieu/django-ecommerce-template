from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Min, Max, Sum, Q

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=2550, blank=True, null=True)
    image = models.ImageField(upload_to='products/categories', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=2550, blank=True, null=True)
    image = models.ImageField(upload_to='products/brands', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=2550, blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Help get info to show product list
    def get_avg_ratings(self):
        avg_rating = Review.objects.filter(product=self).aggregate(Avg('rating')).get('rating__avg')
        return round(avg_rating, 1) if avg_rating is not None else 0

    def get_stars(self):
        avg_ratings = self.get_avg_ratings()

        # Calculate the number of full stars
        full_stars = int(avg_ratings)

        # Calculate the number of half stars
        half_star = 1 if avg_ratings - full_stars >= 0.25 else 0

        # Calculate the number of empty stars
        empty_stars = 5 - full_stars - half_star

        # Create the list with full stars, half stars, and empty stars
        result_list = [1] * full_stars + [0.5] * half_star + [0] * empty_stars

        return result_list

    def get_default_price(self):
        min_price = Price.objects.filter(product=self).aggregate(Min('price')).get('price__min')
        return min_price if min_price is not None else 0


    def __str__(self):
        return self.name




class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color_code = models.CharField(max_length=2550, blank=True, null=True)
    color_image = models.ImageField(upload_to='products/colors', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} {self.color.name}'

    class Meta:
        unique_together = ('product', 'color')


class Version(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2550, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    tech_specs = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} {self.name}'

    def get_split_tech_specs(self):
        items = list(self.tech_specs.items())
        half_len = len(items) - len(items) // 2 # Ưu tiên bên trái dài hơn cho đẹp
        first_half = dict(items[:half_len])
        second_half = dict(items[half_len:])
        return [first_half, second_half]

    class Meta:
        unique_together = ('product', 'name')


class Price(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    product_color = models.ForeignKey(to=ProductColor, on_delete=models.CASCADE, blank=True, null=True)
    version = models.ForeignKey(to=Version, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} {self.price}'

    class Meta:
        unique_together = ('product', 'product_color', 'version')


class Gallery(models.Model):
    media_type = models.CharField(max_length=255, choices=[('Image', 'Image'), ('Video', 'Video')])
    image = models.ImageField(upload_to='products/galleries', blank=True, null=True)
    youtube = models.URLField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} {self.media_type} #{self.pk}'

    class Meta:
        unique_together = ('media_type', 'image', 'youtube', 'product')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(max_length=2550)
    pros = models.CharField(max_length=255, blank=True, null=True)
    cons = models.CharField(max_length=255, blank=True, null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} review {self.rating} {"star" if self.rating == 1 else "stars"} on {self.product}'

    class Meta:
        unique_together = ('product', 'user')

class Inventory(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    version = models.ForeignKey(to=Version, on_delete=models.CASCADE)
    product_color = models.ForeignKey(to=ProductColor, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} {self.version.name} {self.product_color.color.name} ({self.quantity})'

