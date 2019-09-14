from django import forms
from django.forms import TextInput
from .models import (XxgenInsuredDtls,XxgenInsuredAddress,XxgenPolicyDtls,XxgenPolicyVehicleDtls,
                     XxgenPolicyRiskDtls,XxgenPolicyBills)
from Masters.models import XxgenProductRiskMaster
from Masters.models import XxgenVehicleMaster
from datetime import datetime,date, timedelta
import datetime

month = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "may", "6": "June",
             "7": "July", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

class InsuredDtlsForm(forms.ModelForm):

    insured_dob = forms.DateField(widget=forms.SelectDateWidget(months=month,years=range(1980,2050)))

    class Meta:
        model = XxgenInsuredDtls

        fields = [
            'insured_id',
            'insured_name',
            'insured_dob',
            'insured_phone',
            'insured_qualification',
            'insured_profission',
            'email',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by',
            'last_updated_by']

class InsuredAddressForm(forms.ModelForm):
    addr_type = (
        ('', '---------'),
        ('P', ("permanent")),
        ('T', ("Temporary"))
    )
    address_Type = forms.ChoiceField(choices=addr_type, required=False)

    class Meta:
        model = XxgenInsuredAddress
        fields = [
            'address_Type',
            'insured_addr',
            'insured_city',
            'insured_state',
            'insured_country',
            'insured_pincode',
            'created_by',
            'last_updated_by'
        ]

        exclude = ['insured_id',
                   'created_by',
                   'last_updated_by']

class PolicyDtlsForm(forms.ModelForm):
    policy_issued_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 initial=datetime.date.today())

    start_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 initial=datetime.date.today() + timedelta(days=1))
    end_date = forms.DateField(widget=forms.SelectDateWidget(),
                               initial=datetime.date.today() + timedelta(days=365))
    pol_status = (
        ('', '---------'),
        ('QUOTE', ("Quotation")),
        ('PAYMENTPENDING', ("Payment Pending")),
         ('INFORCE', ("Inforce")),
          ('LAPSE', ("Policy Lapse"))
         )
    payment_mode = (
        ('', '---------'),
        ('Q', ("Quartely")),
        ('H', ("Harl Yearly")),
        ('A', ("Annual"))
    )

    policy_status = forms.ChoiceField(choices=pol_status, required=False)
    payment_mode = forms.ChoiceField(choices=payment_mode, required=False)
    policy_no = forms.IntegerField(initial=XxgenPolicyDtls.objects.count()+1)
    renewal_no = forms.IntegerField(initial=0)
    class Meta:
        model = XxgenPolicyDtls
        fields = [
            'policy_no',
            'insured_id',
            'prod_code',
            'agent_code',
            'policy_issued_date',
            'start_date',
            'end_date',
            'policy_status',
            'renewal_no',
            'payment_mode',
            'total_premium',
            'created_by',
            'last_updated_by'
        ]

        exclude = ['created_by',
                   'last_updated_by']

class VehicleDtlsForm(forms.ModelForm):

    mfg_comp = XxgenVehicleMaster.objects.values_list('mfg_company_name',flat=True).distinct()
    mfg_comp_choices = [('', 'None')] + [(id, id) for id in mfg_comp]

    model_id = XxgenVehicleMaster.objects.values_list('model_id', flat=True).distinct()
    model_id_choices = [('', 'None')] + [(id, id) for id in model_id]

    model_name = XxgenVehicleMaster.objects.values_list('model_name', flat=True).distinct()
    model_name_choices = [('', 'None')] + [(id, id) for id in model_name]

    vehicle_make = forms.ChoiceField(choices=mfg_comp_choices, required=False, widget=forms.Select())
    vehicle_model_id = forms.ChoiceField(choices=model_id_choices, required=False, widget=forms.Select())
    vehicle_model_name = forms.ChoiceField(choices=model_name_choices, required=False, widget=forms.Select())

    class Meta:
        model = XxgenPolicyVehicleDtls
        fields = [
            'policy_no',
            'vehicle_year',
            'vehicle_make',
            'vehicle_model_id',
            'vehicle_model_name',
            'chasis_number',
            'engine_number',
            'created_by',
            'last_updated_by'
        ]

        exclude = ['policy_no','created_by',
                   'last_updated_by']


class PolicyRiskDtlsForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 initial=datetime.date.today()+timedelta(days=1))
    end_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 initial=datetime.date.today() + timedelta(days=365))

    class Meta:
        model = XxgenPolicyRiskDtls
        fields = [
            'policy_no',
            'risk_code',
            'risk_description',
            'risk_SA',
            'risk_premium',
            'start_date',
            'end_date',
            'created_by',
            'last_updated_by'
        ]

        exclude = ['policy_no','created_by','last_updated_by']

class PolicyBillsForm(forms.ModelForm):
    class Meta:
        model = XxgenPolicyBills
        fields = [
            'bill_id',
            'policy_no',
            'premium_amount',
            'due_date',
            'balance_amount',
            'created_by',
            'last_updated_by'
        ]
        exclude = ['created_by','last_updated_by','due_date']

