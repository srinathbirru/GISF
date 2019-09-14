from django.urls import path
from .views import (InsuredcreateView,PolicyCreateView,PolicyUpdateView,PolicyBillsview)
from .Utilities import get_risk_details
app_name = 'UnderWriter'

urlpatterns = [
    path('CreateInsured/', InsuredcreateView, name='CreateInsured'),
    path('PolicyCreate/', PolicyCreateView, name='PolicyCreate'),
    path('PolicyUpdate/', PolicyUpdateView, name='PolicyUpdate'),
    path('PolicyBillPay/', PolicyBillsview, name='PolicyBillPay'),

    path('get_risk/', get_risk_details, name='GetRiskDetails'),

    ]
