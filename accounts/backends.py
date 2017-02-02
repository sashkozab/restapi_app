
from .models import MyUser

class SettingsBackend(object):

    def authenticate(self, username=None, password=None):
            try:
                user = MyUser.objects.get(email=username)
                print("Auth.pass: ", password)
                print(user)
                print("Auth.")
                if user.check_password(password):
                    print("Auth.Pass checked")
                    return user
            except MyUser.DoesNotExist:
                return None

    def get_user(self, user_id):
        print("get_user.")
        try:
            user = MyUser.objects.get(pk=user_id)
            print("is user active: ",user.is_active)
            if user.is_active:
                return user
        except MyUser.DoesNotExist:
            print("MyUser.DoesNotExist")
            return None