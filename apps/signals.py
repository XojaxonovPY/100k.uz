from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Order, Payment


@receiver(pre_save, sender=Order)
def cache_old_order(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_order = None
    else:
        try:
            instance._old_order = Order.objects.get(pk=instance.pk)
        except Order.DoesNotExist:
            instance._old_order = None


@receiver(post_save, sender=Order)
def decrease_product_quantity(sender, instance, created, **kwargs):
    product = instance.product

    if created:
        product.quantity -= instance.quantity
        product.order_count += instance.quantity
        product.save()
    else:
        old_order = getattr(instance, '_old_order', None)
        if old_order:
            old_product = old_order.product
            old_quantity = old_order.quantity
            new_quantity = instance.quantity
            new_product = instance.product

            if old_product != new_product:
                old_product.quantity += old_quantity
                old_product.order_count -= old_quantity
                old_product.save()

                new_product.quantity -= new_quantity
                new_product.order_count += new_quantity
                new_product.save()
            else:
                diff = new_quantity - old_quantity
                product.quantity -= diff
                product.order_count += diff
                product.save()


@receiver(post_save, sender=Payment)
def change_user_balance(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        amount = instance.amount
        user.balance -= amount
        user.save()
