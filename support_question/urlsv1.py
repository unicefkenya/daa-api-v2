from django.conf.urls import url

from support_question.views import ListCreateSupportQuestionsAPIView, RetrieveUpdateDestroySupportQuestionAPIView

urlpatterns=[
    url(r'^$',ListCreateSupportQuestionsAPIView.as_view(),name="list_create_support_questions"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroySupportQuestionAPIView.as_view(),name="retrieve_update_destroy_support_question"),
    # url(r'^(?P<pk>[0-9]+)/districts/?$', ListSupportQuestionDistricts.as_view(), name="list_support_question_districts"),

]