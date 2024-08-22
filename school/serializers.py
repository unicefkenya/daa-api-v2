from rest_framework import serializers

from school.models import School, Stream


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("name", "email", "emis_code", "schooling", "county_name", "sub_county_name")


class SchoolSerializer(serializers.ModelSerializer):
    village_name = serializers.CharField(source="village.name", read_only=True)
    district_name = serializers.CharField(source="village.district.name", read_only=True)
    district = serializers.CharField(source="village.district_id", read_only=True)
    sub_county_name = serializers.ReadOnlyField(source="sub_county.name", default=None)
    county = serializers.ReadOnlyField(source="sub_county.county.id", default=None)
    county_name = serializers.ReadOnlyField(source="sub_county.county.name", default=None)

    class Meta:
        model = School
        fields = "__all__"


class SchoolImportError:
    def __init__(self, row_number, error_message, row_details):
        self.row_number = row_number
        self.error_message = error_message
        self.row_details = row_details


class ImportStudentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    admission_no = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    emis_code = serializers.CharField()
    stream = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=20)
    guardian_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    guardian_name = serializers.CharField(max_length=20, required=False, allow_blank=True)
    dob = serializers.DateField(required=False)
    base_class = serializers.CharField(required=False)

    def validate_gender(self, value):
        allowed_gender_values = ["m", "f", "female", "male"]
        if value.lower() not in allowed_gender_values:
            raise serializers.ValidationError("Wrong gender format")
        return "M" if value.lower() in ["m", "male"] else "F"

    def validate_stream(self, value):
        extractedints = list(filter(str.isdigit, value))
        if len(extractedints) < 1:
            raise serializers.ValidationError("Could not get the base_class")
        stream = value[value.index(extractedints[0]) + 1 :]
        base_class = self.validate_base_class(value)
        school = self.validate_emis_code(self.initial_data.get("emis_code", ""))
        streams = list(Stream.objects.filter(school_id=school, name=stream, base_class=base_class))
        stream_id = None
        try:
            if len(streams) < 1:
                sts = Stream.objects.create(name=stream, school_id=school, base_class=base_class)
                stream_id = sts.id
                print(sts)
            else:
                stream_id = streams[0].id
        except Exception as e:
            print(e)
            raise serializers.ValidationError("Failed to Create stream.")

        return stream_id

    def validate_emis_code(self, value):
        if not School.objects.filter(emis_code=value).exists():
            raise serializers.ValidationError("School deos not exist.")
        return School.objects.get(emis_code=value).id

    def validate_base_class(self, value):
        # stream=self.initial_data.get("stream","")
        extractedints = list(filter(str.isdigit, value))
        base_class = extractedints[0] if len(extractedints) > 0 else None
        if not base_class:
            raise serializers.ValidationError("Could not get the base_class")
        return base_class


class ImportDataSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class ImportResults:
    def __init__(self, errors, total_success, total_fails, total_duplicates):
        self.errors = errors
        self.total_duplicates = total_duplicates
        self.total_success = total_success
        self.total_fails = total_fails


class ImportErrorSerializer(serializers.Serializer):
    row_number = serializers.IntegerField()
    error_message = serializers.JSONField()
    row_details = serializers.JSONField(allow_null=True)


class ImportResultsSerializer(serializers.Serializer):
    errors = serializers.ListField(child=ImportErrorSerializer())
    total_success = serializers.IntegerField()
    total_fails = serializers.IntegerField()
    total_duplicates = serializers.IntegerField()
    success_percentage = serializers.SerializerMethodField()

    def get_success_percentage(self, obj):
        total = obj.total_fails + obj.total_success + obj.total_duplicates
        if total == 0:
            return "0%"
        return str(int(obj.total_success / float(total) * 100)) + "%"
