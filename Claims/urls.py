from django.urls import path
from .views import (CalimsRaiseView,SubmitedClaimListView,CalimsProcessView,InprocessClaimListView,SurveyorClaimListView,
                    SurveyProcessView,PaymentPendingClaimListView,process_pending_claims)

app_name = 'Claims1'

urlpatterns = [
    path('RaiseClaim/', CalimsRaiseView, name='RaiseClaim'),
    path('OpenClaimList/', SubmitedClaimListView.as_view(), name='OpenClaimList'),
    path('InProcessClaimList/', InprocessClaimListView.as_view(), name='InProcessClaimList'),
    path('PendingSurvey/', SurveyorClaimListView.as_view(), name='PendingSurvey'),
    path('PendingPayment/', PaymentPendingClaimListView.as_view(), name='PendingPayment'),

    path('<int:claim_id>/ProcessClaim/', CalimsProcessView, name='ProcessClaim1'),
    path('<int:claim_id>/SurveyorClaimListView/', SurveyProcessView, name='SurveyProcess'),
    path('<int:claim_id>/ClaimPay/', process_pending_claims, name='ClaimPay'),


    ]
