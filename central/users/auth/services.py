from users.auth.services import GoogleService
from users.models import User
from django.utils.translation import gettext_lazy as _

class ClanAuthService:
    @staticmethod
    def register():
        pass

    @staticmethod
    def link_google_account(user, id_token):
        try:
            google_user_data = GoogleService.validate(id_token)
            existing_user = User.objects.get(email=google_user_data.get('email')) | User.objects.get(google_id=google_user_data.get('sub'))
            if existing_user:
                if existing_user.id == user.id:
                    user.link_google_account(google_user_data.get('sub'))
                else:
                    raise ValueError(_("This account is already in use."))
            else:
                user.link_google_account(google_user_data.get('sub'))
            return user

        except Exception as e:
            raise e

    @staticmethod
    def link_apple_account(user, id_token):
        pass


