import os
import sys

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from random import randint
from client.models import MyUser
from school.models import School, Teacher, Student, StudentAbsentReason, SchoolsStudentsImport
from school.tasks import import_nemis_data, import_school_students


@receiver(post_save, sender=School, dispatch_uid="school_create_teacher")
def my_school_handler(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]
    if created:
        ###Create the username and password
        try:
            teacher = Teacher.objects.create(
                is_school_admin=True, email=instance.email, first_name="ADMIN", last_name=instance.name, is_non_delete=True, phone=instance.emis_code, school_id=instance.id
            )
            # print("Created Teacher: {}".format(teacher.id))
        except Exception as e:
            print(e)


@receiver(post_save, sender=Teacher, dispatch_uid="teacher_create_credentials")
def my_teacher_handler(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    ###Create the username and password
    if created:
        try:
            username = instance.school.emis_code if instance.is_non_delete else instance.phone
            role = "SCHA" if instance.is_non_delete else "SCHT"
            if instance.email == None or instance.email == "":
                old_password = "admin"
            else:
                old_password = "{}".format(randint(111111, 999999))
            user = MyUser.objects.create_user(
                password=old_password,
                old_password=old_password,
                username=username,
                email=instance.email,
                role=role,
                filter_args="{}".format(instance.school_id),
                first_name=instance.first_name,
                last_name=instance.last_name,
            )
            instance.user_id = user.id
            instance.save()
        except Exception as e:
            print(e)


@receiver(post_delete, sender=Teacher, dispatch_uid="teacher_pre_delete_credentials")
def teacher_pre_delete(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.user_id:
        MyUser.objects.filter(id=instance.user_id).delete()


@receiver(post_save, sender=Student, dispatch_uid="create_update_student")
def student_added(sender, **kwargs):
    instance = kwargs["instance"]
    created = kwargs.get("created", False)


def is_in_test_mode():
    is_testing = "test" in sys.argv
    if is_testing:
        print("Running now in test mode")
    return is_testing


@receiver(post_save, sender=SchoolsStudentsImport, dispatch_uid="on_imports_creation")
def import_added(sender, **kwargs):
    instance = kwargs["instance"]
    created = kwargs.get("created", False)
    if created:
        if instance.import_type == "F":
            if is_in_test_mode():
                import_school_students.task_function(instance.id)
            else:
                import_school_students(instance.id)
        else:
            print(f"Calling nemis {instance.id}")
            if is_in_test_mode():
                import_nemis_data.task_function(instance.id)
            else:
                import_nemis_data(instance.id)


@receiver(post_delete, sender=SchoolsStudentsImport, dispatch_uid="on_delete_stud_import")
def auto_delete_file_on_delete_school_import(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.import_file:
        if os.path.isfile(instance.import_file.path):
            os.remove(instance.import_file.path)

    if instance.errors_file:
        if os.path.isfile(instance.errors_file.path):
            os.remove(instance.errors_file.path)
