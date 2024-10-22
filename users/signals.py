from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm, get_anonymous_user
from .models import UserAddress


@receiver(post_save, sender=UserAddress)
def assign_user_address_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.user:
            assign_perm("change_useraddress", instance.user, instance)
            assign_perm("view_useraddress", instance.user, instance)
            assign_perm("delete_useraddress", instance.user, instance)

        elif instance.anonymous:
            user = get_anonymous_user()
            assign_perm("change_useraddress", user, instance)
            assign_perm("view_useraddress", user, instance)
            assign_perm("delete_useraddress", user, instance)
