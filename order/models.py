from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from account.models import EndUser
from config import settings
from product.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        (0, "PENDING"),
        (1, "ACCEPTED"),
        (2, "DELIVERED"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    products = models.ManyToManyField(Product, related_name="orders")  # Many-to-many relationship
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.STATUS_CHOICES[self.status][1]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if order is new (no primary key yet)

        if not is_new:  # Only send email if order already exists (update)
            old_order = Order.objects.get(pk=self.pk)
            if old_order.status != self.status:  # Only send if status changed
                self.send_status_update_email()

        self.updated_at = timezone.localtime(timezone.now())
        super().save(*args, **kwargs)

    def send_status_update_email(self):
        subject = f"Order Status Update: {self.get_status_display()}"
        message = f"Hello {self.user.name},\n\nYour order number {self.id} is now {self.get_status_display()}."

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )