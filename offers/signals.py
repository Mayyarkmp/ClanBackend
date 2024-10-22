from django.db.models.signals import post_save
from django.dispatch import receiver

from offers.utils import log_purchase
from orders.models import Order  # نفترض وجود نموذج Order

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        # تحقق مما إذا كان الطلب مرتبطًا بعرض أو إعلان
        promotion = instance.promotion  # حسب تصميم نموذج Order
        advertisement = instance.advertisement  # إذا كان مرتبطًا بإعلان

        log_purchase(
            promotion=promotion,
            advertisement=advertisement,
            customer=instance.customer,
            branch=instance.branch,
            region=instance.region,
            platform=instance.platform,
            device=instance.device,
            request=None  # إذا كنت تستطيع تمرير request
        )
