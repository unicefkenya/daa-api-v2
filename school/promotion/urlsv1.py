from django.conf.urls import url

from school.promotion.views import CreateListPromoteSchool, RetrievePromoteSschool, RetrieveCompletePromoteSschool


urlpatterns=[
    url(r'^$', CreateListPromoteSchool.as_view(), name="list_create_promotions"),
    url(r'^(?P<pk>.+)/complete/?$', RetrieveCompletePromoteSschool.as_view(), name="retrieve_complete_undo_promotion"),
    url(r'^(?P<pk>.+)/?$', RetrievePromoteSschool.as_view(), name="retrieve_update_destory_promotion")
    ]