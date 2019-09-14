from django.shortcuts import render,redirect
from django.forms import modelformset_factory
from .forms import InsuredDtlsForm,InsuredAddressForm,PolicyDtlsForm,VehicleDtlsForm,PolicyRiskDtlsForm,PolicyBillsForm
from .models import XxgenPolicyBills,XxgenInsuredDtls,XxgenInsuredAddress,XxgenPolicyVehicleDtls,XxgenPolicyRiskDtls,XxgenPolicyDtls,XxgenPolicyBills,XxgenPolicyAgentComm
from Masters.models import XxgenVehicleMaster
from django.db import transaction, IntegrityError
from .PremiumCalc import motor_Risk_prem_calc,ProRate_prem_calc
from .AgentCommision import Generate_agent_commision
from .Policy_Bills import Generate_invoice
from django.http import JsonResponse
# Create your views here.

def InsuredcreateView(request):
    context = {}
    InsuredAddrFormset = modelformset_factory(XxgenInsuredAddress, form=InsuredAddressForm,extra=2)
    Insuredform = InsuredDtlsForm(request.POST or None)
    formset = InsuredAddrFormset(request.POST or None)

    if request.method == "POST":
        if Insuredform.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    insured = Insuredform.save(commit=False)
                    print('12insured', insured.insured_id)
                    print('12insured', insured.insured_name)
                    insured.save()
                    for mark in formset:
                        data = mark.save(commit=False)
                        if not data.address_Type is None:
                            print('data.address_Type',data.address_Type)
                            print('data.insured_id', data.insured_id)
                            print('34insured',insured)
                            data.insured_id = insured
                            data.save()

            except IntegrityError:
                print("Error Encountered",IntegrityError.__name__)

    Insuredform = InsuredDtlsForm()
    formset = InsuredAddrFormset(queryset=XxgenInsuredAddress.objects.none())

    context = {
        "formset":formset,
        "form":Insuredform
    }
    #context['formset'] = formset
    #context['form'] = Insuredform
    return render(request, 'UW/InsuredCreate.html', context)

def PolicyCreateView(request):
    context = {}

    PolicyForm = PolicyDtlsForm()
    VehicleForm = VehicleDtlsForm()
    RiskFormset = modelformset_factory(XxgenPolicyRiskDtls, form=PolicyRiskDtlsForm, extra=3)

    formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.none())

    if request.method == "POST":

        PolicyForm = PolicyDtlsForm(request.POST or None)
        VehicleForm = VehicleDtlsForm(request.POST or None)
        RiskFormset = modelformset_factory(XxgenPolicyRiskDtls, form=PolicyRiskDtlsForm, extra=3)
        formset = RiskFormset(request.POST or None)

        if PolicyForm.is_valid():
            try:
                with transaction.atomic():
                    policy = PolicyForm.save(commit=False)
                    print('policy no:', policy.policy_no)
                    policy.created_by = str(request.user)
                    policy.last_updated_by = str(request.user)
                    policy.save()

                if VehicleForm.is_valid():
                    vehicle = VehicleForm.save(commit=False)
                    vehicle.created_by = str(request.user)
                    vehicle.last_updated_by = str(request.user)
                    print('vehicle data :', VehicleForm.cleaned_data)
                    vehicle.policy_no = policy
                    vehicle.created_by = str(request.user)
                    vehicle.last_updated_by = str(request.user)
                    print('No policy', vehicle.policy_no)
                    l_year = vehicle.vehicle_year
                    l_make = vehicle.vehicle_make
                    l_model = vehicle.vehicle_model_id
                    l_model_name = vehicle.vehicle_model_name
                    vehicle.save()

                l_tot_prem = 0
                if formset.is_valid():
                    for risk in formset:
                        data = risk.save(commit=False)
                        if not data.risk_code is None:
                            data.policy_no = policy
                            data.created_by = str(request.user)
                            data.last_updated_by = str(request.user)
                            data.risk_description, data.risk_SA, data.risk_premium = \
                                motor_Risk_prem_calc(data.risk_code, l_year, l_make, l_model, l_model_name)
                            l_tot_prem = l_tot_prem + data.risk_premium
                            policy.total_premium = l_tot_prem
                            data.save()

                policy.save()

                if l_tot_prem > 0:
                    Generate_agent_commision(policy.prod_code,
                                             policy.policy_no,
                                             policy.agent_code,
                                             l_tot_prem,
                                             str(request.user))

                    Generate_invoice(policy_no=policy.policy_no,
                                     premium_amount=l_tot_prem,
                                     submit_user=str(request.user))

                psession = XxgenPolicyDtls.objects.get(policy_no=policy.policy_no)
                PolicyForm = PolicyDtlsForm(instance=psession)
                VehicleForm = VehicleDtlsForm(request.POST or None)
                formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.filter(policy_no=policy.policy_no))

            except IntegrityError as e:
                print("Error Encountered", e.__context__)

            except:
                import sys
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                # print('lines',lines)
                print(''.join('!! ' + line for line in lines))
                trx_message = "excetion arised :"

                try:
                    XxgenPolicyBills.objects.filter(policy_no=policy.policy_no).delete()
                    XxgenPolicyAgentComm.objects.filter(policy_no=policy.policy_no).delete()
                    XxgenPolicyRiskDtls.objects.filter(policy_no=policy.policy_no).delete()
                    XxgenPolicyVehicleDtls.objects.filter(policy_no=policy.policy_no).delete()
                    XxgenPolicyDtls.objects.filter(policy_no=policy.policy_no).delete()
                except:
                    print('Transaction revertion exception')

            finally:
                # Sometimes you want to ensure some cleanup code executes even if an exception was raised somewhere along the way. For example, you may have a database connection that you want to close once you're done. Here is the wrong way to do it:
                print('Finally BLock Executed')

    context['Policyform'] = PolicyForm
    context['VehicleForm'] = VehicleForm
    context['PolicyRishForm'] = formset

    return render(request, 'UW/CreatePolicy.html', context)


def PolicyUpdateView(request):
    context = {}

    if request.method == "GET":
        search_id = request.GET.get('Sid')
        print('search_id', search_id)

        if request.GET.get('Sid') != "None" \
                or not request.GET.get('Sid') is None:
            try:
                psession = XxgenPolicyDtls.objects.get(policy_no=request.GET.get('Sid'))
                PolicyForm = PolicyDtlsForm(instance=psession)
                RiskFormset = modelformset_factory(XxgenPolicyRiskDtls, form=PolicyRiskDtlsForm, extra=3)
                formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.filter(policy_no=request.GET.get('Sid')))

            except XxgenPolicyRiskDtls.DoesNotExist :
                PolicyForm = PolicyDtlsForm()
                formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.none())

                context['Policyform'] = PolicyForm
                context['PolicyRishForm'] = formset
                return render(request, 'UW/Policy_Update.html', context)

            except XxgenPolicyDtls.DoesNotExist :
                print('not exist exception')
                PolicyForm = PolicyDtlsForm()
                RiskFormset = modelformset_factory(XxgenPolicyRiskDtls, form=PolicyRiskDtlsForm, extra=3)
                formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.none())

                context['Policyform'] = PolicyForm
                context['PolicyRishForm'] = formset
                return render(request, 'UW/Policy_Update.html', context)

        else:
            PolicyForm = PolicyDtlsForm()
            RiskFormset = modelformset_factory(XxgenPolicyRiskDtls, form=PolicyRiskDtlsForm, extra=3)
            formset = RiskFormset(queryset=XxgenPolicyRiskDtls.objects.none())
            context['Policyform'] = PolicyForm
            context['PolicyRishForm'] = formset
            return render(request, 'UW/Policy_Update.html', context)

    if request.method == "POST":

        psession = XxgenPolicyDtls.objects.get(policy_no=request.GET.get('Sid'))
        PolicyForm = PolicyDtlsForm(request.POST,instance=psession)

        RiskFormset = modelformset_factory(XxgenPolicyRiskDtls,form=PolicyRiskDtlsForm, extra=3)
        formset = RiskFormset(request.POST)

        if PolicyForm.is_valid():
            print(PolicyForm.cleaned_data)

            policy = PolicyForm.save(commit=False)
            policy.created_by = str(request.user)
            policy.last_updated_by = str(request.user)
            policy.save()

            l_tot_prem = policy.total_premium
            if formset.is_valid():
                for risk in formset:
                    data = risk.save(commit=False)
                    data.policy_no=policy
                    if not data.risk_code is None:
                        l_risk_year_prem = 0
                        if not XxgenPolicyRiskDtls.objects.filter(policy_no=data.policy_no,risk_code=data.risk_code).exists():
                            vobj = XxgenPolicyVehicleDtls.objects.get(policy_no=data.policy_no)
                            data.risk_description, data.risk_SA, l_risk_year_prem = \
                                motor_Risk_prem_calc(data.risk_code, vobj.vehicle_year, vobj.vehicle_make, vobj.vehicle_model_id, vobj.vehicle_model_name)
                            data.risk_premium = ProRate_prem_calc(l_risk_year_prem, policy.end_date)
                            data.policy_no = policy
                            l_tot_prem = l_tot_prem + data.risk_premium
                            data.created_by = str(request.user)
                            data.last_updated_by = str(request.user)
                            data.save()

                policy.total_premium=l_tot_prem
                policy.save()

    context['Policyform'] = PolicyForm
    context['PolicyRishForm'] = formset
    return render(request, 'UW/Policy_Update.html', context)

def PolicyBillsview(request):
    context = {}

    if request.method == "GET":
        search_id = request.GET.get('Sid')
        print('search_id', search_id)
        policyBill = PolicyBillsForm()
        if request.GET.get('Sid') != "None":
            try:
                psession = XxgenPolicyBills.objects.get(policy_no=request.GET.get('Sid'))
                print('psession',psession)
                policyBill = PolicyBillsForm(instance=psession)
                context['policyBill'] = policyBill
            except XxgenPolicyBills.DoesNotExist:
                policyBill = PolicyBillsForm()
                context['policyBill'] = policyBill
                return render(request, 'UW/Policy_Bills.html', context)
        else:
            policyBill = PolicyBillsForm()
            context['policyBill'] = policyBill
            return render(request, 'UW/Policy_Bills.html', context)

    if request.method == "POST":
        psession = XxgenPolicyBills.objects.get(policy_no=request.GET.get('Sid'))
        policyBill = PolicyBillsForm(request.POST, instance=psession)
        if policyBill.is_valid():
            print(policyBill.cleaned_data)

            policy = policyBill.save(commit=False)
            print('policy no:', policy.policy_no)
            policy.created_by = str(request.user)
            policy.last_updated_by = str(request.user)
            policy.save()


            policyBill = PolicyBillsForm()
            context['policyBill'] = policyBill
            context['message'] = 'Payment is successfully done....'

            obj, created = XxgenPolicyDtls.objects.update_or_create(
                policy_no=policy.policy_no,
                defaults={'policy_status': 'INFORCE'})

    return render(request, 'UW/Policy_Bills.html', context)

