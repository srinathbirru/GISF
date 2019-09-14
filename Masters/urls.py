from django.urls import path
from .views import (createAgent, AgentCommision, ProductsMaster, ProductRisk, VehicleMasterView,
                    VehicleDepriciationMasterView,XxgenNcbMasterView,ClaimStatusMasterView,
                    ClaimsSurveyorMasterView,ClaimStatusListView)

app_name = 'Masters'

urlpatterns = [
    path('ProductsMaster/', ProductsMaster, name='ProductsMaster'),
    path('ProductRisk/', ProductRisk, name='ProductRisk'),  # modelformset_factory table format
    path('createAgent/', createAgent, name='createAgent'),
    path('AgentCommision/', AgentCommision, name='AgentCommision'),  # modelformset_factory table format
    path('VehicleMaster/', VehicleMasterView, name='VehicleMaster'),
    path('VehicleDepriciation/', VehicleDepriciationMasterView, name='VehicleDepriciation'),
    path('NcbMaster/', XxgenNcbMasterView, name='NcbMaster'),
    path('ClaimStatus/', ClaimStatusMasterView, name='ClaimStatus'),
    path('SurveyorMaster/', ClaimsSurveyorMasterView, name='SurveyorMaster'),
    path('ClaimsStatusList/', ClaimStatusListView.as_view(), name='ClaimsStatusList'),





   ]