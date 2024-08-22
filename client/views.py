from datetime import timedelta
from random import randint

from django.core.mail import send_mail
from django.db.models import Subquery, BooleanField
from django.db.models import Value
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken, Application
from oauthlib.common import generate_token
from rest_framework.renderers import TemplateHTMLRenderer

from client.filters import UsersFilter
from client.models import MyUser
from client.serializers import (
    MyUserSerializer,
    GooglePlusSerializer,
    ForgotPasswordSerializer,
    ChangePasswordSerializer,
    ResetPasswordserializer,
    AccountVerifySerializer,
    PasswordResetForEbnumeratorSerializer,
    ResetTeacherPasswordSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import status

from mylib.my_common import MySendEmail, MyCustomException, MyDjangoFilterBackend, MyStandardPagination
from mylib.mygenerics import MyListCreateAPIView

from rest_framework import generics


# Email
from wvapi.settings import MY_SITE_URL


class CreateListUser(generics.ListCreateAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    pagination_class = MyStandardPagination
    filter_mixin = UsersFilter

    def perform_create(self, serializer):
        serializer.save(old_password=serializer.initial_data.get("password"), confirm_code=randint(111111, 999999))


class RetrieveUpdateUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


class RetrieveUpdateClient(generics.RetrieveUpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return MyUser.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        sdata = self.get_update_data()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=sdata, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_update_data(self):
        ##Check if its from social login
        sdata = None
        type = self.request.query_params.get("type", None)
        if type == "google-plus":
            ser = GooglePlusSerializer(data=self.request.data)
            ser.is_valid(raise_exception=True)
            sdata = ser.data
        else:
            sdata = self.request.data
        return sdata


class ChangePasswordAPiView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.confirm_old_password(serializer)
        self.request.user.set_password(serializer.validated_data.get("new_password"))
        self.request.user.changed_password = True
        self.request.user.save()
        return Response({"detail": "Password successfully changed."})

    def confirm_old_password(self, serializer):
        old_password = serializer.validated_data.get("old_password")
        valid = self.request.user.check_password(old_password)
        if not valid:
            raise MyCustomException("Wrong old password provided.")
        return True


class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordserializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # self.object = self.get_object()
        serializer.is_valid(raise_exception=True)
        cls = list(MyUser.objects.filter(reset_code=serializer.validated_data.get("reset_code")))
        if not len(cls) > 0:
            raise MyCustomException("User not Found")
        self.object = cls[0].id
        # Check old password
        # if not self.object.check_password(serializer.data.get("old_password")):
        #     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        new_password = serializer.data.get("new_password")
        cls[0].set_password(new_password)
        cls[0].save()
        cls[0].reset_code = None
        cls[0].save()
        return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        user = MyUser.objects.get(username=username)
        reset_code = randint(111111, 999999)
        user.reset_code = reset_code
        user.save()
        name = user.first_name
        try:
            data = {"name": name, "reset_code": reset_code}
            MySendEmail("Onekana Digital Attendance Password Reset Code", "forgot.html", data, [user.email])
            return Response({"detail": "Reset code sent successfully.", "email": user.email})
        except Exception as e:
            print(e)
            return Response({"detail": "Failed to send email."})


class ResendVerifyEmailView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, format=None):
        client = get_object_or_404(MyUser, id=self.request.user.id)
        try:
            self.send_confirm_email(client)
            return Response({"detail": "Email sent successfully."})
        except:
            return Response({"detail": "Failed to send email."})

    def send_confirm_email(instance):
        user = instance.user
        token = generate_token()
        app = Application.objects.first()
        AccessToken.objects.create(user=user, application=app, expires=now() + timedelta(days=1), token=token)
        link = "%s/verify-account?token=%s&confirm_code=%s" % (MY_SITE_URL, token, instance.confirm_code)
        data = {"name": user.first_name, "verify_url": link}
        MySendEmail("Adeso Account Verification", "new_user.html", data, [user.username])


class ResetTeacherPassword(APIView):
    allowed_roles = ["SCHT", "SCHA", "RO"]
    serializer_class = ResetTeacherPasswordSerializer

    def put(self, request, format=None):
        serializer = ResetTeacherPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_my_user(serializer)
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        return Response({"detail": "Password reset successful"})

    def get_my_user(self, serializer):
        lookup_url_kwarg = "username"
        queryset = MyUser.objects.all()
        filter_kwargs = {"username": serializer.validated_data.get("username")}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj


class VerifyAccountView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        data = {}
        data["token"] = request.query_params.get("token")
        data["confirm_code"] = request.query_params.get("confirm_code")
        serializer = AccountVerifySerializer(data=data)
        valid = serializer.is_valid()
        failed_data = {"response": "Token expired . Try resending the verification email", "heading": "Verification failed."}

        if not valid:
            print("Not valid", serializer.errors)
            return Response(failed_data, template_name="verify_account.html")
        token = serializer.validated_data.get("token")
        tokens = list(AccessToken.objects.filter(token=token))
        if len(tokens) != 1:
            print("No token...")
            return Response(failed_data, template_name="verify_account.html")
        token = tokens[0]
        ###check if expired
        print(token)
        ####
        clients = MyUser.objects.filter(id=token.user_id)
        if len(clients) != 1:
            return Response(failed_data, template_name="verify_account.html")

        if clients[0].verified:
            return Response({"response": "Account already verified.", "heading": "Account active"}, template_name="verify_account.html")
        clients[0].verified = True
        clients[0].save()
        return Response({"response": "Account verified.", "heading": "Success"}, template_name="verify_account.html")
