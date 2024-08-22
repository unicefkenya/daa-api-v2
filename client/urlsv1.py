from django.conf.urls import url

from client.activity_logs.views import ListActivityLogs, ExportActivityLogs
from client.users.views import ListCreateAdminCredentials, RetrieveUpdateSystemUser
from client.views import RetrieveUpdateClient, CreateListUser, ForgotPasswordView, \
    ChangePasswordAPiView, ResetPasswordView, ResendVerifyEmailView, RetrieveUpdateUser, ResetTeacherPassword
from school.teacher.views import RetrieveSchoolInfoAPIView

urlpatterns=[
    url(r'^$',ListCreateAdminCredentials.as_view(),name="list_create_system_users"),
    # url(r'^s$', ListCreateAdminCredentials.as_view(), name="ListCreateAdminCredentials"),
    url(r'^logs/?$', ListActivityLogs.as_view(), name="list_activity_logs"),
    url(r'^logs/export/?$', ExportActivityLogs.as_view(), name="export_activity_logs"),
    url(r'^me/?$',RetrieveUpdateClient.as_view(),name="retrieve_update_client"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateSystemUser.as_view(),name="retrieve_update_client"),
    url(r'^me/profile/?$',RetrieveUpdateClient.as_view(),name="Retrieve_client"),
    url(r'^me/change-password', ChangePasswordAPiView.as_view(), name="clients_change_password"),
    url(r'^me/resend-verification-email', ResendVerifyEmailView.as_view(), name="clients_resend_confirm_email"),
    url(r'^forgot-password', ForgotPasswordView.as_view(), name="clients_forgot_password"),
    url(r'^reset-password', ResetPasswordView.as_view(), name="clients_reset_password"),
    url(r'^admin-reset-password/?$', ResetTeacherPassword.as_view(), name="admin_reset_enum_password"),
    url(r'^teacher/school-info/?$', RetrieveSchoolInfoAPIView.as_view(), name="user_teacher_school_info"),
]
