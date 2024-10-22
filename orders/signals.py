from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, get_anonymous_user

from .models import Order, Cart, CartItem
from .tasks import send_order_statistics_task


@receiver(post_save, sender=Cart)
def assign_cart_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.customer:
            assign_perm("change_cart", instance.customer, instance)
            assign_perm("view_cart", instance.customer, instance)
            assign_perm("delete_cart", instance.customer, instance)

        elif instance.anonymous:

            user = get_anonymous_user()
            assign_perm("change_cart", user, instance)
            assign_perm("view_cart", user, instance)
            assign_perm("delete_cart", user, instance)


@receiver(post_save, sender=CartItem)
def assign_cart_item_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.cart.customer:
            assign_perm("change_cartitem", instance.cart.customer, instance)
            assign_perm("view_cartitem", instance.cart.customer, instance)
            assign_perm("delete_cartitem", instance.cart.customer, instance)

        elif instance.cart.anonymous:

            user = get_anonymous_user()
            assign_perm("change_cartitem", user, instance)
            assign_perm("view_cartitem", user, instance)
            assign_perm("delete_cartitem", user, instance)


@receiver(post_save, sender=Order)
def send_order_statistics(sender, instance, created, **kwargs):
    if created:
        pass
        # send_order_statistics_task().delay()
