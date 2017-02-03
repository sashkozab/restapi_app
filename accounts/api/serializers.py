from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q



from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    CharField,
    EmailField
    )


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }

    def create(self, validated_data):
        print("validated_data: ", validated_data)
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                # username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]
        print("FirstData: ",data)
        if not email:
            raise ValidationError("A email is required.")
        user = User.objects.filter(
                Q(email=email)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        print("User from validate: ", user)
        print("is user exists: ", user.exists(), "user count : ", user.count)
        if user.exists():
            print("password: ", password)
            user_obj = user.first()
        else:
            print("Hello")
            raise ValidationError("This email is not valid")
        print("user_obj: ", user_obj)
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials.")
        data["token"] = "Some token"
        print("Data: ",data)
        return data
