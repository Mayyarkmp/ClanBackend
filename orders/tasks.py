from .models import Order, Cart
from celery import shared_task
from guardian.shortcuts import get_objects_for_user
from users.models import User
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def get_order_statistics(user_uid, start_datetime=None, end_datetime=None):
    user = User.objects.get(uid=user_uid)

    if end_datetime is None:
        end_datetime = timezone.now()

    # إذا تم تحديد يوم فقط بدون وقت
    if start_datetime is not None and isinstance(start_datetime, str):
        try:
            start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d')
            end_datetime = start_datetime + timedelta(days=1) - timedelta(seconds=1)
        except ValueError:
            raise ValueError("Please provide a valid date in 'YYYY-MM-DD' format")

    if start_datetime is None:
        start_datetime = end_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    orders = get_objects_for_user(user, 'orders.view_order', klass=Order)
    carts = get_objects_for_user(user, 'orders.view_cart', klass=Cart)

    order_counts = orders.values('status').annotate(count=Count('id'))
    cart_counts = carts.values('status').annotate(count=Count('id'))
    order_result = {order['status']: order['count'] for order in order_counts}
    order_result['total'] = orders.count()
    cart_result = {cart['status']: cart['count'] for cart in cart_counts}
    cart_result['total'] = carts.count()

    result = {}
    result['orders'] = order_result
    result['carts'] = cart_result
    return result


@shared_task
def send_order_statistics_task():
    # استدعاء الإحصائيات عبر Celery وإرسالها عبر WebSocket
    for user in User.objects.filter(is_superuser=True):
        statistics = get_order_statistics.delay(user_uid=user.uid)

        # استخدام async_to_sync لإرسال البيانات عبر WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'order_{user.uid}',
            {
                'type': 'send_statistics',  # يجب أن يكون لديك handler لهذا النوع في الـ consumer
                'statistics': statistics.get()  # انتظر حتى انتهاء مهمة Celery لجلب الإحصائيات
            }
        )
