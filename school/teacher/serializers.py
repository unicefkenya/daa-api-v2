from rest_framework import serializers

from school.models import Teacher, Stream, School
from school.stream.serializers import StudentsStreamSerializer




class TeacherSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source="school.name",read_only=True)
    username=serializers.CharField(source="user.username",read_only=True)
    gender_name = serializers.CharField(source="user.get_gender_display", read_only=True)
    gender = serializers.CharField(source="user.gender", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    role_name = serializers.CharField(source="user.get_role_display", read_only=True)



    class Meta:
        model=Teacher
        fields=("__all__")



class TeacherSchoolInfoSerializer(TeacherSerializer):
    streams=serializers.SerializerMethodField()
    teachers=serializers.SerializerMethodField()

    def get_streams(self, obj):
        if obj.is_school_admin:
            queryset = Stream.objects.filter(school_id=obj.school_id).order_by("base_class").prefetch_related("students")
        else:
            queryset = obj.streams.all().prefetch_related("students")
        ser = StudentsStreamSerializer(queryset, many=True)
        return ser.data

    def get_teachers(self,obj):
        if obj.is_school_admin:
            queryset=Teacher.objects.filter(school_id=obj.school_id).select_related("user","school")
        else:
            queryset=[]
        ser=TeacherSerializer(queryset,many=True)
        return ser.data
