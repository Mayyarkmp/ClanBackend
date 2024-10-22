from .models import Room, Message

class RoomService:
    @staticmethod
    def get_rooms():
        return Room.objects.all()


class MessageService:
    @staticmethod
    def get_messages(room_id):
        return Message.objects.filter(room_id=room_id)

    @staticmethod
    def get_messages(sender_id, room_id):
        return Message.objects.filter(sender_id=sender_id, room_id=room_id)



