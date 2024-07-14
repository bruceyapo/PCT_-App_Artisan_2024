from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model




class TelephoneBackend(BaseBackend):
    def authenticate(self, request, numero_de_telephone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(numero_de_telephone= numero_de_telephone)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
