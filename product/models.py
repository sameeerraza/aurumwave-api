from django.db import models
from django.utils import timezone
from account.models import EndUser
from utils.misc import product_image_directory_path


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=510)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=75, null=True)
    image = models.ImageField(upload_to=product_image_directory_path, blank=True, null=True)
    available_amount = models.PositiveIntegerField(default=1)
    sold_amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="products")

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        (0, "PENDING"),
        (1, "ACCEPTED"),
        (2, "DELIVERED"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(
        EndUser, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.STATUS_CHOICES[self.status][1]

    def save(self, *args, **kwargs):
        if not self.pk:  # only set on creation
            self.created_at = timezone.localtime(timezone.now())
        self.updated_at = timezone.localtime(timezone.now())
        super().save(*args, **kwargs)
