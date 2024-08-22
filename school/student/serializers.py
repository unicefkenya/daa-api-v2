import datetime

from django.utils import timezone
from rest_framework import serializers, fields
from rest_framework.serializers import ModelSerializer
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from school.models import Student, SPECIAL_NEEDS, StudentDeleteReason, StudentAbsentReason
from school.special_needs.serializers import SpecialNeedSerializer


class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="stream.school.name", read_only=True)
    stream_name = serializers.CharField(source="stream.name", read_only=True)
    base_class = serializers.CharField(source="stream.base_class", read_only=True)
    full_name = serializers.ReadOnlyField()
    student_id = serializers.ReadOnlyField()
    date_enrolled = serializers.DateField(default=datetime.date.today)
    special_needs_details = SpecialNeedSerializer(many=True, source="special_needs", read_only=True)
    county = serializers.ReadOnlyField(source="sub_county.county_id")
    guardian_county = serializers.ReadOnlyField(source="guardian_sub_county.county_id")
    age = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField(source="get_status_display")
    gender_display = serializers.ReadOnlyField(source="get_gender_display")

    county_name = serializers.ReadOnlyField(source="sub_county.county.name", default="N/A")
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name", default="N/A")

    # Guardian
    guardian_county_name = serializers.ReadOnlyField(source="guardian_sub_county.county.name", default="N/A")
    guardian_sub_county_name = serializers.ReadOnlyField(source="guardian_sub_county.name", default="N/A")
    guardian_status_display = serializers.ReadOnlyField(source="get_guardian_status_display")

    class Meta:
        model = Student
        fields = "__all__"


class SimpleStudentAbsentSerializer(serializers.ModelSerializer):
    reason_name = serializers.CharField(source="reason.name")
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    student_id = serializers.ReadOnlyField()
    special_needs_details = SpecialNeedSerializer(many=True, source="special_needs", read_only=True)

    class Meta:
        model = StudentAbsentReason
        fields = ("reason", "reason_name", "id", "age", "full_name", "student_id", "special_needs_details")


class AbsentStudentSerializer(StudentSerializer):
    reason_absent = serializers.SerializerMethodField()

    def get_reason_absent(self, obj):
        date = self.context.get("request").query_params.get("date")
        if date:
            re = list(StudentAbsentReason.objects.filter(date=date, student_id=obj.id))
            if len(re) > 0:
                return SimpleStudentAbsentSerializer(re[0]).data
        return None


class SimpleStudentSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = ("first_name", "last_name", "id", "age")


class DeleteStudentSerializer(serializers.ModelSerializer):
    dropout_reason = serializers.CharField(source="reason.name", read_only=True)
    first_name = serializers.CharField(source="student.first_name", read_only=True)
    stream_name = serializers.CharField(source="student.stream.name", read_only=True)
    base_class = serializers.CharField(source="student.stream.base_class", read_only=True)
    school = serializers.CharField(source="student.stream.school", read_only=True)
    school_emis_code = serializers.CharField(source="student.stream.school.emis_code", read_only=True)
    school_name = serializers.CharField(source="student.stream.school.name", read_only=True)
    middle_name = serializers.CharField(source="student.middle_name", read_only=True)
    last_name = serializers.CharField(source="student.last_name", read_only=True)
    admission_no = serializers.CharField(source="student.admission_no", read_only=True)
    reason_description = serializers.CharField(source="reason.description", read_only=True)

    class Meta:
        model = StudentDeleteReason
        fields = "__all__"


class BulkStudentSerializer(BulkSerializerMixin, ModelSerializer):
    school_name = serializers.CharField(source="stream.school.name", read_only=True)
    stream_name = serializers.CharField(source="stream.name", read_only=True)
    base_class = serializers.CharField(source="stream.base_class", read_only=True)
    full_name = serializers.ReadOnlyField()
    student_id = serializers.ReadOnlyField()
    date_enrolled = serializers.DateField(default=datetime.date.today)
    special_needs_details = SpecialNeedSerializer(many=True, source="special_needs", read_only=True)
    county = serializers.ReadOnlyField(source="sub_county.county_id")
    guardian_county = serializers.ReadOnlyField(source="guardian_sub_county.county_id")
    age = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField(source="get_status_display")
    gender_display = serializers.ReadOnlyField(source="get_gender_display")

    county_name = serializers.ReadOnlyField(source="sub_county.county.name", default="N/A")
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name", default="N/A")

    # Guardian
    guardian_county_name = serializers.ReadOnlyField(source="guardian_sub_county.county.name", default="N/A")
    guardian_sub_county_name = serializers.ReadOnlyField(source="guardian_sub_county.name", default="N/A")
    guardian_status_display = serializers.ReadOnlyField(source="get_guardian_status_display")

    class Meta(object):
        model = Student
        fields = "__all__"
        # only necessary in DRF3
        list_serializer_class = BulkListSerializer


class EnrollmentSerializer(serializers.Serializer):
    males = serializers.IntegerField()
    females = serializers.IntegerField()
    dropout_males = serializers.IntegerField()
    dropout_females = serializers.IntegerField()
    value = serializers.CharField()
    total = serializers.SerializerMethodField()
    active_total = serializers.SerializerMethodField()
    dropout_total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj["males"] + obj["females"] + obj["dropout_males"] + obj["dropout_females"]

    def get_active_total(self, obj):
        return obj["males"] + obj["females"]

    def get_dropout_total(self, obj):
        return obj["dropout_males"] + obj["dropout_females"]

    def to_representation(self, instance):
        # data = super(EnrollmentSerializer, self).to_representation(instance)
        return instance
