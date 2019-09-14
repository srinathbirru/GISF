from django import forms
from django.forms import TextInput
from .models import (XxgenClaims)
from Masters.models import XxgenProductRiskMaster,XxgenClaimStatusMaster
from UnderWriter.models import XxgenPolicyRiskDtls,XxgenPolicyDtls
from Claims.models import XxgenClaimsProcessDtls,XxgenClaimsSurveyorDtls,XxgenClaimsDocs,XxgenClaimsPayments
from Masters.models import XxgenClaimsSurveyorMaster
from datetime import datetime,date, timedelta
import datetime

class CalimsRaiseForm(forms.ModelForm):

    policy_no =  forms.IntegerField()
    claim_id = forms.IntegerField(initial=XxgenClaims.objects.count()+1)
    claim_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 initial=datetime.date.today() + timedelta(days=1))

    RiskCode = XxgenProductRiskMaster.objects.values_list('risk_code', flat=True).filter(prod_code='MOTOR').distinct()
    RiskCode_choices = [('', 'None')] + [(id,id) for id in RiskCode]
    claim_risk = forms.ChoiceField(choices=RiskCode_choices, required=False, widget=forms.Select())

    class Meta:
        model = XxgenClaims
        fields = [
            'claim_id',
            'policy_no',
            'claim_date',
            'claim_risk',
            'amount_claimed',
            'amount_setteled',
            'total_policy_amount',
            'date_of_settele',
            'total_policy_amount',
            'total_claim_amount',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by','last_updated_by','amount_setteled',
            'total_policy_amount',
            'date_of_settele',
            'total_policy_amount',
            'total_claim_amount']
        print('before clean')

    def clean(self):
        # data from the form is fetched using super function
        super(CalimsRaiseForm, self).clean()

        policyNO = self.cleaned_data.get('policy_no')
        print('policyNO',policyNO)

        if not XxgenPolicyDtls.objects.filter(policy_no=policyNO).exists():
            print('inside policyNO', policyNO)
            self._errors['policy_no'] = self.error_class([
                'Not a valid policy'])

        Riskcode = self.cleaned_data.get('claim_risk')
        print('Riskcode',Riskcode)
        if not XxgenPolicyRiskDtls.objects.filter(risk_code=Riskcode).exists():
            print('inside if', Riskcode)
            self._errors['claim_risk'] = self.error_class([
                'Your policy not coverd this risk'])
        return self.cleaned_data


class CalimsProcessForm(forms.ModelForm):

    clm_process_id = forms.IntegerField()
    claim = forms.IntegerField()
    policy_no = forms.IntegerField()
    claim_date = forms.DateField()

    claim_statusCode = XxgenClaimStatusMaster.objects.values_list('clm_status_code', flat=True)
    claim_status_choices = [('', 'None')] + [(id, id) for id in claim_statusCode]
    claim_status = forms.ChoiceField(choices=claim_status_choices, required=False, widget=forms.Select())

    class Meta:
        model = XxgenClaimsProcessDtls
        fields = [
            'clm_process_id',
            'claim',
            'policy_no',
            'claim_date',
            'amount_claimed',
            'amount_setteled',
            'date_of_settele',
            'total_policy_amount',
            'total_claim_amount',
            'claim_status',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by', 'last_updated_by']

class CalimsSurveyorForm(forms.ModelForm):

    Surveyor_id = XxgenClaimsSurveyorMaster.objects.values_list('surveyor_id', flat=True)
    Surveyor_id_choices = [('', 'None')] + [(id, id) for id in Surveyor_id]
    surveyor = forms.ChoiceField(choices=Surveyor_id_choices, required=False, widget=forms.Select())

    clm_status = XxgenClaimStatusMaster.objects.values_list('clm_status_code', flat=True)
    clm_status_choices = [('', 'None')] + [(id, id) for id in clm_status]
    clm_survey_status = forms.ChoiceField(choices=clm_status_choices, required=False, widget=forms.Select())



    surveyor_comments = forms.CharField(required=False,widget=forms.Textarea(
                                    attrs={"placeholder" : "your Comments ",
                                            "rows" : 10,
                                            "cols" : 50,
                                           "width": "100 %",
                                           'style': 'height: 5em;'
                                           }
                                ))

    class Meta:
        model = XxgenClaimsSurveyorDtls
        fields = [
            'surveyor',
            'claim',
            'surveyor_comments',
            'surveyor_claim_amount',
            'clm_survey_status',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by', 'last_updated_by','claim']

    def clean_surveyor(self):
        # data from the form is fetched using super function
        super(CalimsSurveyorForm, self).clean()
        sid = self.cleaned_data.get('surveyor')
        surveror_id= XxgenClaimsSurveyorMaster.objects.get(surveyor_id=sid)
        return surveror_id



class CalimsDocumentForm(forms.ModelForm):

    doc_description = forms.CharField(widget=forms.Textarea(
                                    attrs={"rows" : 20,
                                           "rows": 10,
                                           "width": "100 %",
                                           'style': 'height: 3em;width: "100 %"'
                                           }
                                ))

    class Meta:
        model = XxgenClaimsDocs
        fields = [
            'doc_type_code',
            'doc_description',
            'claim',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by', 'last_updated_by','claim']


class CalimsPaymentsForm(forms.ModelForm):

    date_of_piad = forms.DateField(widget=forms.SelectDateWidget(),
                                         initial=datetime.date.today())
    class Meta:
        model = XxgenClaimsPayments
        fields = [
            'payment_receipt_id',
            'claim',
            'amount_piad',
            'date_of_piad',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by', 'last_updated_by','claim']

    def clean_claim(self):
        # data from the form is fetched using super function
        super(CalimsPaymentsForm, self).clean()
        sid = self.cleaned_data.get('claim')
        claim= XxgenClaims.objects.get(claim_id=sid)
        return claim