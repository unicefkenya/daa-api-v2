from rest_framework import serializers


from client.models import MyUser
from mylib.image import Base64ImageField


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class AccountVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
    confirm_code = serializers.IntegerField(allow_null=True)


class PasswordResetForEbnumeratorSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    detail = serializers.ReadOnlyField()

    def validate_username(self, value):
        users = list(MyUser.objects.filter(username=value))
        if len(users) != 1:
            raise serializers.ValidationError("User does not exist. Please contact support.")
        user = users[0]
        if user.email == None or user.email == "":
            raise serializers.ValidationError("No email set for user. Please contact support.")
        return value


class ResetPasswordserializer(serializers.Serializer):
    reset_code = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_confirm_password(self, value):
        if self.initial_data.get("new_password") != value:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def validate_reset_code(self, value):
        if not MyUser.objects.filter(reset_code=value).exists():
            raise serializers.ValidationError("Reset code Invalid or Expired")
        return value


class ResetTeacherPasswordSerializer(serializers.Serializer):
    allowed_roles = ["SCHT", "SCHA", "RO"]
    username = serializers.CharField()
    new_password = serializers.CharField()

    def validate_username(self, value):
        if not MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("User does not exist.")
        user = MyUser.objects.get(username=value)
        if user.role not in self.allowed_roles:
            raise serializers.ValidationError("Admin assisted password reset is for teacher accounts only.")
        return value


class MyUserSerializer(serializers.ModelSerializer):
    # chart_settings=ChartSettingSerializer(many=True,read_only=True)
    image = Base64ImageField(required=False, max_length=None, use_url=True)
    profile_image = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    role_name = serializers.CharField(source="get_role_display", read_only=True)
    teacher = serializers.IntegerField(source="teacher.id", read_only=True)
    is_school_admin = serializers.BooleanField(source="teacher.is_school_admin", read_only=True)
    school = serializers.IntegerField(source="teacher.school_id", read_only=True)
    school_name = serializers.CharField(source="teacher.school.name", read_only=True)
    emis_code = serializers.CharField(source="teacher.school.emis_code", read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = MyUser
        fields = (
            "id",
            "first_name",
            "full_name",
            "dummy",
            "filter_args",
            "is_school_admin",
            "teacher",
            "school",
            "school_name",
            "emis_code",
            "role_name",
            "last_name",
            "username",
            "dob",
            "changed_password",
            "role",
            "image",
            "email",
            "phone",
            "gender",
            "password",
            "profile_image",
            "gender_display",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            # 'google_profile_image':{'write_only':True}
        }

    def get_gender_display(self, obj):
        return obj.get_gender_display()

    def get_profile_image(self, obj):
        defauly_image = "http://pronksiapartments.ee/wp-content/uploads/2015/10/placeholder-face-big.png"
        if obj.image:
            return obj.image
        if obj.google_profile_image:
            return obj.google_profile_image
        return defauly_image

    def create(self, validated_data):
        # print(validated_data)
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def validate_username(self,value):
    #   if MyUser.objects.filter(username=value).exists():
    #     raise serializers.ValidationError("User with username alteady exists")
    #   return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class GooglePlusSerializer(serializers.Serializer):
    familyName = serializers.CharField(max_length=45, required=False, allow_null=True)
    givenName = serializers.CharField(max_length=45, required=False, allow_null=True)
    imageUrl = serializers.URLField(max_length=200, required=False, allow_null=True)

    def to_representation(self, instance):

        return {"first_name": instance["givenName"], "last_name": instance["familyName"], "google_profile_image": instance["imageUrl"]}
