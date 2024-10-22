from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm
from guardian.utils import get_anonymous_user
from .models import DeliveryTypeContents
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=DeliveryTypeContents)
def set_delivery_type_content_permissions(sender, instance, **kwargs):
    anonymous_user = get_anonymous_user()
    content_type = ContentType.objects.get_for_model(DeliveryTypeContents)
    perm = f'{content_type.app_label}.view_{content_type.model}'

    if not instance.is_draft and instance.is_default:
        assign_perm(perm, anonymous_user, instance)
    else:
        remove_perm(perm, anonymous_user, instance)
