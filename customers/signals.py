from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import BrowsingKey


# @receiver(post_save, sender=BrowsingKey, dispatch_uid='create_user_profile')
# def c