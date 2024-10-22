from rest_framework.permissions import BasePermission
from .models import BrowsingKey


class BrowsingKeyPermission(BasePermission):
    """
    إذن يسمح فقط للطلبات التي تحتوي على browsing_key مع branch أو zone.
    """

    def has_permission(self, request, view):
        # الحصول على browsing_key من الطلب (من معلمات الطلب أو الرؤوس مثلاً)
        browsing_key_value = request.headers.get("Browsing-Key")

        # التأكد من وجود browsing_key في الطلب
        if not browsing_key_value:
            return False

        # التحقق من وجود browsing_key في قاعدة البيانات
        try:
            browsing_key = BrowsingKey.objects.get(key=browsing_key_value)
        except BrowsingKey.DoesNotExist:
            return False

        # التحقق من وجود branch أو zone
        if browsing_key.branch or browsing_key.zone:
            return True

        # إذا لم تكن هناك branch أو zone، نرفض الطلب
        return True
