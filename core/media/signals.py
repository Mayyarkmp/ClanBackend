from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Media
from django.contrib.auth.models import AnonymousUser
from guardian.shortcuts import assign_perm, get_anonymous_user


@receiver(post_save, sender=Media)
def give_permissions_to_media(sender, instance, created, **kwargs):
    if created:
        anonymous_user = get_anonymous_user()
        assign_perm("view_media", anonymous_user, instance)
