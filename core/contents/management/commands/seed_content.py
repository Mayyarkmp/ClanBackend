from django.core.management.base import BaseCommand
from core.contents.models import DeliveryTypeContents

class Command(BaseCommand):
    help = 'Create delivery type contents'

    def handle(self, *args, **kwargs):
        # إنشاء كائن توصيل سريع
        fast_delivery = DeliveryTypeContents.objects.create(
            type=DeliveryTypeContents.DeliveryType.FAST,
            name="توصيل سريع",
            short_description="توصيل سريع للطلبات.",
            description="نحن نقدم خدمة التوصيل السريع لضمان وصول طلباتك في أسرع وقت.",
            name_en="Fast Delivery",
            short_description_en="Fast delivery for orders.",
            description_en="We offer fast delivery service to ensure your orders arrive as quickly as possible.",
            is_draft=False,
            is_default=True
        )

        # إنشاء كائن توصيل مجدول
        scheduled_delivery = DeliveryTypeContents.objects.create(
            type=DeliveryTypeContents.DeliveryType.SCHEDULED,
            name="توصيل مجدول",
            short_description="توصيل في الوقت المحدد.",
            description="نحن نقدم خدمة التوصيل المجدول لضمان وصول طلباتك في الوقت الذي تحدده.",
            name_en="Scheduled Delivery",
            short_description_en="Delivery at scheduled time.",
            description_en="We provide scheduled delivery service to ensure your orders arrive at the time you specify.",
            is_draft=False,
            is_default=False
        )

        self.stdout.write(self.style.SUCCESS('تم إنشاء كائنين توصيل بنجاح!'))
