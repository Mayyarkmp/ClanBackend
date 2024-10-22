import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .tasks import get_order_statistics
from users.models import User


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.user_uid = self.scope['url_route']['kwargs']['user_uid']
            self.room_group_name = f'order_{self.user_uid}'

            # إضافة المستخدم إلى الغرفة المناسبة
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # إزالة المستخدم من الغرفة عند قطع الاتصال
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")

        if action == "statistics":
            start_datetime = text_data_json.get('start_datetime', None)
            end_datetime = text_data_json.get('end_datetime', None)
            user_uid = self.user.uid

            # استدعاء مهمة Celery لجلب الإحصائيات
            statistics = await sync_to_async(get_order_statistics)(
                user_uid=user_uid,
                start_datetime=start_datetime if start_datetime else None,
                end_datetime=end_datetime if end_datetime else None
            )

            # إرسال الإحصائيات للمستخدم
            await self.send(text_data=json.dumps({
                'type': 'statistics',
                'action': 'update',
                'statistics': statistics
            }))

    async def send_statistics(self, event):
        statistics = event['statistics']

        # إرسال البيانات المحدثة للمستخدم عبر WebSocket
        await self.send(text_data=json.dumps({
            'type': 'statistics',
            'action': 'update',
            'statistics': statistics
        }))
