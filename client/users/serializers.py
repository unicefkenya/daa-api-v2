from rest_framework import serializers

from client.models import MyUser, SCHOOL_ADMIN, SUB_COUNTY_ADMIN, COUNTY_ADMIN, SCHOOL_TEACHER
from client.serializers import MyUserSerializer


class RoleBasedCharField(serializers.CharField):
    @staticmethod
    def _validate_phone_number(value):
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            raise serializers.ValidationError("Phone number must contain 11 digits.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(args)
        # print(kwargs)
        # print(self.initial)
        # self.validators.append(PhoneNumberField._validate_phone_number)

    def to_internal_value(self, data):
        print(data)
        data = super().to_internal_value(data)
        return data


class SystemUserSerializer(MyUserSerializer):
    # school=serializers.CharField()
    # sub_county=serializers.CharField()
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        data = kwargs.get("data", None)
        if data is not None:
            role = data.get("role", None)
            if role == SCHOOL_ADMIN or role == SCHOOL_TEACHER:
                # self.fields.update({"school":serializers.CharField(required=True)})
                self.fields.update({"school": serializers.ListField(child=serializers.CharField(required=True), required=True)})
            elif role == SUB_COUNTY_ADMIN:
                self.fields.update({"sub_county": serializers.ListField(child=serializers.CharField(required=True), required=True)})
            elif role == COUNTY_ADMIN:
                self.fields.update({"county": serializers.ListField(child=serializers.CharField(required=True), required=True)})

    def create(self, validated_data):
        # super(SystemUsersCountyTests ,self).setUp()
        role = validated_data.get("role")
        id = None
        if role == SCHOOL_ADMIN or role == SCHOOL_TEACHER:
            id = validated_data.get("school")
            validated_data.pop("school")
            self.fields.pop("school")

        elif role == COUNTY_ADMIN:
            id = validated_data.get("county")
            validated_data.pop("county")
            self.fields.pop("county")

        elif role == SUB_COUNTY_ADMIN:
            id = validated_data.get("sub_county")
            validated_data.pop("sub_county")
            self.fields.pop("sub_county")

        if id != None:
            args = ""
            if type(id) == list:
                args = ",".join(id)
            else:
                args = id
            # print(type(id), args)
            validated_data["filter_args"] = args

        # print(validated_data)
        return super().create(validated_data)
