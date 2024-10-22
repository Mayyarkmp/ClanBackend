from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from central.users.models import CentralUser

# @receiver(post_save, sender=ClanUser, dispatch_uid='clan_user_create')
# def create_clan_staff_assigned_branches(sender, instance, created, **kwargs):
#     if created:
#         if sender.is_clan and sender.