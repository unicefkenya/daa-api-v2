from symbol import pass_stmt
from rest_framework import generics
from region.models import SubCounty
from region.sub_countys.serializers import SubCountySerializer
from rest_framework.permissions import IsAuthenticated
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, filter_queryset_based_on_role
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
import mylib.my_common as my_common
class ListCreateSubCountysAPIView(generics.ListCreateAPIView):
    serializer_class = SubCountySerializer
    queryset = SubCounty.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryser = super(ListCreateSubCountysAPIView, self).get_queryset()
        return filter_queryset_based_on_role(queryset=queryser, user_id=self.request.user.id)


class UpdateSubCountyPartnersAPIView(generics.CreateAPIView):
    serializer_class = SubCountySerializer
    queryset = SubCounty.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        partners=User.objects.filter(is_partner=True)
        ## Reset all the partners names 
        ids=SubCounty.objects.update(partner_names=None)
        # print(ids)
        
        for partner in partners:
            try:
                sub_counties=my_common.get_filters_as_array(partner.filter_args)
                # print(sub_counties)
                sub_counties=SubCounty.objects.filter(id__in=sub_counties)
                for sub_county in sub_counties:
                    if sub_county.partner_names !=None:
                        sub_county.partner_names= f"{sub_county.partner_names},{partner.username.upper()}" 
                    else:
                        sub_county.partner_names= partner.username.upper()
                    sub_county.save()
            except Exception as e:
                print(e)
        
        return Response({"detail":"Update Done."})
    
    pass
class RetrieveUpdateDestroySubCountyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCountySerializer
    queryset = SubCounty.objects.all()
    permission_classes = (IsAuthenticated,)
