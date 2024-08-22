import functools
from datetime import date
from django.db.models import CharField
from django.utils import timezone
from rest_framework import serializers

from client.serializers import MyUserSerializer
from mylib.my_common import tuple_choices_to_map
from school.models import SchoolsStudentsImport, STUDENT_STATUS, STUDENT_GENDERS
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.db.models.functions import Lower

from wvapi.settings import LEARNER_MIN_AGE, LEARNER_MAX_AGE

CharField.register_lookup(Lower)


class empty:
    """
    This class is used to represent no data being provided for a given input
    or output value.

    It is required because `None` may be a valid input or output value.
    """

    pass


class SchoolsStudentsImportSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%a, %d %b %y %I:%M %p", read_only=True)
    modified = serializers.DateTimeField(format="%a, %d %b %y %I:%M %p", read_only=True)
    step_display = serializers.ReadOnlyField(source="get_step_display")
    user_details = MyUserSerializer(source="user", read_only=True)
    clean = serializers.ReadOnlyField()
    is_clean = serializers.ReadOnlyField()
    raw_data = serializers.JSONField(required=False, write_only=True)
    # url = serializers.ReadOnlyField(source="errors_file.url")
    # url_name = serializers.ReadOnlyField(source="errors_file.name")

    class Meta:
        model = SchoolsStudentsImport
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}


STUDENTS_ALL_STATUS = (
    *STUDENT_STATUS,
    ("NE", "Never Enrolled OOSC"),
    ("NE", "Newly Enrolled"),
    ("PE", "Previously Enrolled"),
    ("OOSC", "Out of School"),
    ("OOSC", "Previously Enrolled OOSC (Dropped out of school previously)"),
)

StudentstatusChoices = tuple_choices_to_map(STUDENTS_ALL_STATUS)

GENDER_CHOICES = (
    *STUDENT_GENDERS,
    ("M", "Boy"),
    ("M", "Boys"),
    ("F", "Girl"),
    ("F", "Girls"),
)
studentGenderChoices = tuple_choices_to_map(GENDER_CHOICES)

# print(StudentstatusChoices)
# print(studentGenderChoices)


def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


DJANGO_DATE_INPUT_FORMATS = ["%Y-%m-%d %H:%M:%S %p", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S ", "%m/%d/%Y %H:%M:%S %p", "%m/%d/%Y"]


class StudentSchoolSerializer(serializers.Serializer):
    school = serializers.CharField()
    school_nemis_code = serializers.CharField()
    county = serializers.CharField()
    school_ownership = serializers.CharField(required=False, allow_null=True)
    subcounty = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    gender = serializers.CharField()
    stream = serializers.CharField()

    status = serializers.CharField(required=True, allow_null=True)

    # Guardian
    father_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mother_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    guardian_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    guardian_county = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    guardian_subcounty = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    learner_county = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    learner_subcounty = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    level_name = serializers.CharField(required=False, allow_null=True)
    guardian_email = serializers.EmailField(required=False, allow_null=True)

    date_enrolled = serializers.DateTimeField(
        input_formats=DJANGO_DATE_INPUT_FORMATS,
        allow_null=True,
        default=timezone.now,
    )

    date_of_birth = serializers.DateTimeField(
        input_formats=DJANGO_DATE_INPUT_FORMATS,
        required=False,
        allow_null=True,
    )

    guardian_phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    special_needs = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    admission_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    upi = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    distance_from_school = serializers.CharField(required=False, allow_null=True)
    village = serializers.CharField(required=False, allow_null=True)

    def is_valid(self, raise_exception=False):
        """
        Method overriden to ignore errors from wron date format for date_enrolled and date_of_birth
        Once the issue is fixed on nemis, this is no longer required
        """
        is_ser_valid = super(StudentSchoolSerializer, self).is_valid(raise_exception=raise_exception)
        # print(is_ser_valid)
        error_fields_to_reset_to_null = ["date_of_birth", "date_enrolled"]
        if not is_ser_valid:
            errors_fields = self.errors.keys()
            for field in errors_fields:
                if field in error_fields_to_reset_to_null:
                    # print(f"Resetting {field}")
                    try:
                        self.initial_data.pop(field)
                        self.errors.pop(field)
                        # print(f"Done Reset {field}")
                    except Exception as e:
                        print(e)
        self._errors = {}
        try:
            self._validated_data = self.run_validation(self.initial_data)
        except ValidationError as exc:
            self._validated_data = {}
            self._errors = exc.detail
        else:
            self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        return not bool(self._errors)

    def validate_gender(self, value):
        allowed_gender_values = ["m", "f", "female", "male"]
        if value.lower() not in allowed_gender_values:
            raise serializers.ValidationError("Wrong gender format")
        return "M" if value.lower() in ["m", "male"] else "F"

    def validate_level_name(self, value):
        if value == None:
            return value
        if "primary" not in value.lower():
            raise serializers.ValidationError("School level should be primary")
        return value

    def validate_distance_from_school(self, value):
        if value == None:
            return None

        strings = value.split(" ")
        extractedstring = list(filter(str.isdigit, map(lambda v: "".join(list(filter(str.isdigit, v))), strings)))
        extractedints = list(map(lambda x: int(x), extractedstring))
        total = functools.reduce(lambda a, b: a + b, extractedints)
        # print(extractedints,total)
        return "{}".format(int(total / len(extractedints)))

    def validate_status(self, value):
        if value == None:
            return "PE"

        status = StudentstatusChoices.get(value.lower().strip())
        if status:
            return status
        else:
            return "PE"

    def validate_stream(self, value):
        if "pp" in value.lower():
            raise serializers.ValidationError("Only Class/Grade 1-8")
        if "form" in value.lower():
            raise serializers.ValidationError("Only Class/Grade 1-8")

        return value

    def validate_date_enrolled(self, value):
        # print(f"Enroll {value}")
        if value == None:
            return timezone.now()
        return value

    def validate_date_of_birth(self, value):
        # print(f"DoB {value}")
        # print(f"validatin date {value}")
        if value == None:
            return None
        age = calculateAge(value)
        # print(age)
        if age < LEARNER_MIN_AGE:
            raise serializers.ValidationError("Learner's date of birth less than {} years".format(LEARNER_MIN_AGE))

        if age > LEARNER_MAX_AGE:
            raise serializers.ValidationError("Learner's date of birth more than {} years".format(LEARNER_MAX_AGE))
        return value


class SchoolImportSerializer(serializers.Serializer):
    school = serializers.CharField()
    school_nemis_code = serializers.CharField()
    county = serializers.CharField()
    subcounty = serializers.CharField()
