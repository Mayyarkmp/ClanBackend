from users.auth.services import GoogleService

class CustomerAuthService:
    @staticmethod
    def link_google_account(user, id_token):
        try:
            google_user_data = GoogleService.validate(id_token)
            user.link_google_account(google_user_data.get('sub'))
            if not user.email:
                user.email = google_user_data.get('email')
                user.is_email_verified = True
            if not user.first_name:
                user.first_name = google_user_data.get('given_name')
            if not user.last_name:
                user.last_name = google_user_data.get('family_name')


            return user

        except Exception as e:
            raise e

