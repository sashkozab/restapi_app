from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from django.core import exceptions


from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    CharField,
    EmailField,
    Serializer
    )


User = get_user_model()
# from accounts.models import MyUser

class UserCreateSerializer(HyperlinkedModelSerializer):
    password = CharField(write_only=True, required=True)
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
                # email = email
                email=validated_data['email'],
                password=validated_data['password']
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

# class UserLoginSerializer(ModelSerializer):
#     token = CharField(allow_blank=True, read_only=True)
#     email = EmailField(label='Email Address')
#     password = CharField(write_only=True, required=True)
#     class Meta:
#         model = User
#         fields = [
#             'email',
#             'password',
#             'token',
            
#         ]
#         extra_kwargs = {"password":
#                             {"write_only": True}
#                             }
#     def validate(self, data):
#         user_obj = None
#         email = data.get("email")
#         password = data["password"]
#         print("FirstData: ",data)
#         if not email:
#             raise ValidationError("A email is required.")
#         user = User.objects.filter(
#                 Q(email=email)
#             ).distinct()
#         user = user.exclude(email__isnull=True).exclude(email__iexact='')
#         print("User from validate: ", user)
#         print("is user exists: ", user.exists(), "user count : ", user.count)
#         if user.exists() and user.count() == 1:
#             print("password: ", password)
#             user_obj = user.first()
#         else:
#             print("Hello")
#             raise ValidationError("This email is not valid")
#         print("user_obj: ", user_obj)
#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise ValidationError("Incorrect credentials.")
#         data["token"] = "Some token"
#         print("Data: ",data)
#         print("Pass: ", data["password"])
#         return data


class AuthTokenSerializer(Serializer):
    email = EmailField()
    password = CharField(style={'input_type': 'password'})

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
        email = data.get('email')
        password = data.get('password')
        username = User.objects.get(email=email).username

        if email and password:
            print("Email;Pass: ", email, password)
            user = authenticate(email=email, password=password)
            # user = User.objects.filter(
            #     Q(email=email)
            # ).distinct()
            print("User: ", user)

            # if user:
            #     if not user.is_active:
            #         msg = ('User account is disabled.')
            #         raise exceptions.ValidationError(msg)
            # else:
            #     msg = ('Unable to log in with provided credentials.')
            #     raise exceptions.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data