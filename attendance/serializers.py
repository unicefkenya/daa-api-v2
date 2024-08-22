from rest_framework import serializers

from attendance.models import Attendance, TeacherAttendance
from school.models import Stream, Student, Teacher


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class TakeAttendanceSerializer(serializers.Serializer):
    present = serializers.ListField(child=serializers.IntegerField())
    absent = serializers.ListField(child=serializers.IntegerField())
    date = serializers.DateField()


class StreamAttendanceSerializer(serializers.Serializer):
    present = serializers.ListField(child=serializers.IntegerField(), required=True)
    absent = serializers.ListField(child=serializers.IntegerField(), required=True)
    date = serializers.DateField()
    stream = serializers.CharField()
    moe_sync = serializers.BooleanField(default=False)

    def validate_stream(self, value):
        return value
        # Todo: Validate for teachers as well
        if Stream.objects.filter(id=value).exists():
            return value
        raise serializers.ValidationError("Stream with id {} does not exist.".format(value))

    def validate_present(self, value):
        return value
        # Todo: Validate for teachers as well

        stream = ""  # self.initial_data.get("stream")
        if stream == "teachers":
            return list(Teacher.objects.filter(active=True, id__in=value))
        return list(Student.objects.filter(active=True, id__in=value).values_list("id", flat=True))

    def validate_absent(self, value):
        return value
        stream = self.initial_data.get("stream")
        if stream == "teachers":
            return list(Teacher.objects.filter(active=True, id__in=value))

        return list(Student.objects.filter(active=True, id__in=value).values_list("id", flat=True))

    def raise_error(error):
        raise serializers.ValidationError(error)

    def create(self, validated_data):
        return self.save_validated_date(validated_data)

    def save_validated_date(self, validated_data):
        ###Makes Sure only one attendance per day
        attendance_date = validated_data.get("date")
        stream = validated_data.get("stream")
        now = str(attendance_date).replace("-", "")

        ###Prepare Attendances Instances
        presents = validated_data.get("present")
        absents = validated_data.get("absent")

        # Check if the stream is teachers
        if stream == "teachers":
            present_teacher_attendances = [
                TeacherAttendance(
                    date=attendance_date,
                    status=1,
                    teacher_id=teach_id,
                    id="T{}{}".format(now, teach_id),
                )
                for teach_id in presents
            ]

            absent_teacher_attendances = [
                TeacherAttendance(
                    date=attendance_date,
                    status=1,
                    teacher_id=teach_id,
                    id="T{}{}".format(now, teach_id),
                )
                for teach_id in absents
            ]

            bulk_teacher_creates = []
            present_ids = [at.id for at in present_teacher_attendances]
            update_present_teachers_attendance_ids = list(TeacherAttendance.objects.filter(id__in=present_ids).values_list("id", flat=True))
            bulk_teacher_creates = bulk_teacher_creates + [at for at in present_teacher_attendances if at.id not in update_present_teachers_attendance_ids]

            absent_teacher_ids = [at.id for at in absent_teacher_attendances]
            update_absent_teacher_attendance_ids = list(TeacherAttendance.objects.filter(id__in=absent_teacher_ids).values_list("id", flat=True))
            bulk_teacher_creates = bulk_teacher_creates + [at for at in absent_teacher_attendances if at.id not in update_absent_teacher_attendance_ids]

            # Update the Teacher Attendance
            TeacherAttendance.objects.filter(id__in=update_present_teachers_attendance_ids).update(status=1)
            TeacherAttendance.objects.filter(id__in=update_absent_teacher_attendance_ids).update(status=0)

            ##Bulk Create Attendances
            # print("Bulk creating {}".format(len(bulk_creates)))
            TeacherAttendance.objects.bulk_create(bulk_teacher_creates)

            validated_data["moe_sync"] = False
            return validated_data

        # Prepare bulk creates and Updates
        present_attendances = [Attendance(date=attendance_date, id=now + str(stud_id), student_id=stud_id, status=1, stream_id=stream) for stud_id in presents]

        absent_attendances = [Attendance(date=attendance_date, id=now + str(stud_id), student_id=stud_id, status=0, stream_id=stream) for stud_id in absents]

        bulk_creates = []
        present_ids = [at.id for at in present_attendances]
        update_present_attendance_ids = list(Attendance.objects.filter(id__in=present_ids).values_list("id", flat=True))
        bulk_creates = bulk_creates + [at for at in present_attendances if at.id not in update_present_attendance_ids]

        absent_ids = [at.id for at in absent_attendances]
        update_absent_attendance_ids = list(Attendance.objects.filter(id__in=absent_ids).values_list("id", flat=True))
        bulk_creates = bulk_creates + [at for at in absent_attendances if at.id not in update_absent_attendance_ids]

        ###Bulk Update the Attendances
        # print("Bulk Updating {}".format(len(update_present_attendance_ids+update_absent_attendance_ids)))
        # Check if present in both absents and presents
        Attendance.objects.filter(id__in=update_present_attendance_ids).update(status=1)
        Attendance.objects.filter(id__in=update_absent_attendance_ids).update(status=0)

        ##Bulk Create Attendances
        # print("Bulk creating {}".format(len(bulk_creates)))
        for att in bulk_creates:
            try:
                att.save()
            except Exception as e:
                print(e)
        # Attendance.objects.bulk_create(bulk_creates)

        # res = take_update_moe_attendance(validated_data)
        # validated_data["moe_sync"] = res
        return validated_data

    def save(self, **kwargs):
        assert hasattr(self, "_errors"), "You must call `.is_valid()` before calling `.save()`."
        assert not self.errors, "You cannot call `.save()` on a serializer with invalid data."
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        return self.save_validated_date(validated_data)


class SerializerAll(serializers.Serializer):
    value = serializers.CharField()
    present_males = serializers.IntegerField()
    present_females = serializers.IntegerField(
        allow_null=True,
    )
    absent_males = serializers.IntegerField()
    absent_females = serializers.IntegerField()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total = obj["present_males"] + obj["present_females"] + obj["absent_males"] + obj["absent_females"]
        return total

    def to_representation(self, instance):
        # #print instance,self.get_total(instance)
        stud = self.context.get("student")
        type = self.context.get("type")
        if stud:
            return {"present": instance["present_males"] + instance["present_females"], "absent": instance["absent_males"] + instance["absent_females"], "total": int(self.get_total(instance)), "value": instance["value"]}
        return super(SerializerAll, self).to_representation(instance)


class SerializerAllPercentages(serializers.Serializer):
    value = serializers.CharField()
    present_males = serializers.IntegerField(write_only=True)
    present_females = serializers.IntegerField(allow_null=True, write_only=True)
    absent_males = serializers.IntegerField(write_only=True)
    absent_females = serializers.IntegerField(write_only=True)
    total = serializers.SerializerMethodField()

    def get_males_total(self, obj):
        return float(obj["present_males"] + obj["absent_males"])

    def get_gender_total(self, obj, field):
        # Get the gender from
        gender = field.split("_")[-1]
        return float(obj["present_" + gender] + obj["absent_" + gender])

    def get_total(self, obj):
        total = float(obj["present_males"] + obj["present_females"] + obj["absent_males"] + obj["absent_females"])
        return total

    def males_present(self, obj):
        return self.get_total(obj)

    def get_percentage(self, obj, field):
        total = obj[field + "_females"] + obj[field + "_males"]
        if total == 0:
            return 0
        return round((total / self.get_total(obj)) * 100, 2)

    def get_pm(self, obj, field):
        if self.get_gender_total(obj, field=field) == 0:
            return 0
        return round((obj[field] / self.get_gender_total(obj, field=field)) * 100, 2)
        # return round((obj[field]/self.get_total(obj))*100,2)

    def to_representation(self, instance):
        ##print instance,self.get_total(instance)
        stud = self.context.get("student")
        type = self.context.get("type")
        return_type = self.context.get("return_type")
        # print ("return type",return_type)
        if stud or return_type == "count":
            return {
                "present": instance["present_males"] + instance["present_females"],
                "present_males": instance["present_males"],
                "present_females": instance["present_females"],
                "absent": instance["absent_males"] + instance["absent_females"],
                "absent_males": instance["absent_males"],
                "absent_females": instance["absent_females"],
                "total": int(self.get_total(instance)),
                "value": instance["value"],
            }
        return {
            "present_males": self.get_pm(instance, "present_males"),
            "present_females": self.get_pm(instance, "present_females"),
            "absent_males": self.get_pm(instance, "absent_males"),
            "absent_females": self.get_pm(instance, "absent_females"),
            "present": self.get_percentage(instance, "present"),
            "absent": self.get_percentage(instance, "absent"),
            "total": 100,
            "value": instance["value"],
        }
