from django.shortcuts import render
from .forms import CalimsRaiseForm,CalimsProcessForm,CalimsSurveyorForm,CalimsDocumentForm,CalimsPaymentsForm
# Create your views here.
from django.views.generic import (ListView)
from .models import XxgenClaims,XxgenClaimsProcessDtls,XxgenClaimsDocs,XxgenClaimsSurveyorDtls,XxgenClaimsPayments
from django.forms import modelformset_factory

class SubmitedClaimListView(ListView):

    template_name = 'XxgenClaims_list.html'
    queryset = XxgenClaims.objects.filter(claim_status='SUBMITTED')

class InprocessClaimListView(ListView):
    template_name = 'XxgenClaims_list.html'
    queryset = XxgenClaims.objects.exclude(claim_status__in = ['SUBMITTED','CLOSED','REJECTED'])


class SurveyorClaimListView(ListView):
    template_name = 'XxgenClaimsSurveyorDtls_list.html'
    queryset = XxgenClaimsSurveyorDtls.objects.filter(clm_survey_status__in=['UNDERSURVEY','SURVEYORASSIGNED','DOCUMENTPENDING'])

class PaymentPendingClaimListView(ListView):
    template_name = 'XxgenClaimsProcessDtls_list.html'
    queryset = XxgenClaimsProcessDtls.objects.filter(claim_status='PAYMENTPENDING')


def CalimsRaiseView(request):
    context = {}

    ClaimForm = CalimsRaiseForm(request.POST or None)
    if request.method == "POST":
        if ClaimForm.is_valid():
            print(ClaimForm.cleaned_data)

            claim = ClaimForm.save(commit=False)
            print('policy no:', claim.policy_no)
            claim.created_by = str(request.user)
            claim.claim_status = 'SUBMITTED'
            claim.last_updated_by = str(request.user)
            claim.save()

            ClaimForm = CalimsRaiseForm()
    context['ClaimForm'] = ClaimForm

    def get_initial(self):
        return {
            'id_policy_no': 1
        }

    return render(request, 'Claims/Claim_Raise.html', context)

def CalimsProcessView(request,**kwargs):
    context = {}
    ClaimForm = CalimsProcessForm()
    claimSurveyForm = CalimsSurveyorForm()

    ClmDocForm = modelformset_factory(XxgenClaimsDocs, form=CalimsDocumentForm, extra=2)
    formset = ClmDocForm(request.POST or None)


    claimid = kwargs.get("claim_id")


    if not XxgenClaimsProcessDtls.objects.filter(claim=claimid).exists():

        obj = XxgenClaims.objects.get(claim_id=claimid)


        XxgenClaimsProcessDtls.objects.create(clm_process_id=XxgenClaimsProcessDtls.objects.count()+1,
                                              claim = obj.claim_id,
                                              policy_no = obj.policy_no,
                                              claim_date = obj.claim_date,
                                              amount_claimed = obj.amount_claimed,
                                              claim_status = obj.claim_status
                                              )

        obj, created = XxgenClaims.objects.update_or_create(
            claim_id=claimid, policy_no=obj.policy_no,
            defaults={'claim_status': 'INPROCESS'},
        )


    if request.method == "GET":
        print('inside get')
        try:
            inst = XxgenClaimsProcessDtls.objects.get(claim=claimid)
            ClaimForm = CalimsProcessForm(instance=inst)
            sinst = XxgenClaimsSurveyorDtls.objects.get(claim=claimid)
            claimSurveyForm = CalimsSurveyorForm(instance=sinst)

            ClmDocForm = modelformset_factory(XxgenClaimsDocs, form=CalimsDocumentForm, extra=2)
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.filter(claim=claimid))

        except XxgenClaimsSurveyorDtls.DoesNotExist:
            claimSurveyForm = CalimsSurveyorForm()
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.none())
            print('XxgenClaimsSurveyorDtls')
        except XxgenClaimsDocs.DoesNotExist:
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.none())
            print('XxgenClaimsDocs')

    if request.method == "POST":
        inst = XxgenClaimsProcessDtls.objects.get(claim=claimid)
        ClaimForm = CalimsProcessForm(request.POST or None, instance=inst)


        if ClaimForm.is_valid():
            print(ClaimForm.cleaned_data)

            claim = ClaimForm.save(commit=False)
            claim.created_by = str(request.user)
            claim.last_updated_by = str(request.user)
            claim.save()

            if not XxgenClaimsSurveyorDtls.objects.filter(claim=claimid).exists():
                claimSurveyForm = CalimsSurveyorForm(request.POST)
            else:
                sinst = XxgenClaimsSurveyorDtls.objects.get(claim=claimid)
                claimSurveyForm = CalimsSurveyorForm(request.POST, instance=sinst)

            if claimSurveyForm.is_valid():
                surveyor = claimSurveyForm.save(commit=False)
                surveyor.created_by = str(request.user)
                surveyor.last_updated_by = str(request.user)
                surveyor.claim = claim.claim
                surveyor.clm_survey_status = claim.claim_status
                surveyor.created_by = str(request.user)
                surveyor.last_updated_by = str(request.user)
                surveyor.save()

                obj, created = XxgenClaims.objects.update_or_create(
                    claim_id=claimid,
                    defaults={'claim_status': surveyor.clm_survey_status,
                              'amount_setteled': surveyor.surveyor_claim_amount,
                              'Remarks': surveyor.surveyor_comments
                              }
                )

                obj, created = XxgenClaimsProcessDtls.objects.update_or_create(
                    claim=claimid,
                    defaults={'claim_status': surveyor.clm_survey_status,
                              'amount_setteled': surveyor.surveyor_claim_amount
                              }
                )


                if formset.is_valid():
                    for sur in formset:
                        data = sur.save(commit=False)
                        if not data.doc_type_code is None:
                            data.claim = claim.claim

                            data.created_by = str(request.user)
                            data.last_updated_by = str(request.user)
                            data.save()


        ClaimForm = CalimsProcessForm()
        claimSurveyForm = CalimsSurveyorForm()

    context['ClaimForm'] = ClaimForm
    context['claimSurveyForm'] = claimSurveyForm
    context['formset'] = formset


    return render(request, 'Claims/Claim_Process.html', context)

def SurveyProcessView(request,**kwargs):
    context = {}

    claimSurveyForm = CalimsSurveyorForm()
    ClmDocForm = modelformset_factory(XxgenClaimsDocs, form=CalimsDocumentForm, extra=2)
    formset = ClmDocForm(request.POST or None)

    claimid = kwargs.get("claim_id")

    if request.method == "GET":
        print('inside get')
        try:

            sinst = XxgenClaimsSurveyorDtls.objects.get(claim=claimid)
            claimSurveyForm = CalimsSurveyorForm(instance=sinst)

            ClmDocForm = modelformset_factory(XxgenClaimsDocs, form=CalimsDocumentForm, extra=2)
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.filter(claim=claimid))

        except XxgenClaimsSurveyorDtls.DoesNotExist:
            claimSurveyForm = CalimsSurveyorForm()
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.none())

        except XxgenClaimsDocs.DoesNotExist:
            formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.none())


    if request.method == "POST":

        sinst = XxgenClaimsSurveyorDtls.objects.get(claim=claimid)
        claimSurveyForm = CalimsSurveyorForm(request.POST,instance=sinst)

        ClmDocForm = modelformset_factory(XxgenClaimsDocs,form=CalimsDocumentForm, extra=3)
        formset = ClmDocForm(request.POST)

        if claimSurveyForm.is_valid():
            surveyor = claimSurveyForm.save(commit=False)
            surveyor.created_by = str(request.user)
            surveyor.last_updated_by = str(request.user)
            surveyor.created_by = str(request.user)
            surveyor.last_updated_by = str(request.user)
            surveyor.save()

            obj, created = XxgenClaims.objects.update_or_create(
                claim_id=claimid,
                defaults={'claim_status': surveyor.clm_survey_status,
                          'amount_setteled':surveyor.surveyor_claim_amount,
                          'Remarks':surveyor.surveyor_comments
            }
            )

            obj, created = XxgenClaimsProcessDtls.objects.update_or_create(
                claim=claimid,
                defaults={'claim_status': surveyor.clm_survey_status,
                          'amount_setteled': surveyor.surveyor_claim_amount
                          }
            )

            if formset.is_valid():
                for risk in formset:
                    data = risk.save(commit=False)
                    if not data.doc_type_code is None:
                        data.claim = surveyor.claim
                        data.created_by = str(request.user)
                        data.last_updated_by = str(request.user)
                        data.save()


        claimSurveyForm = CalimsSurveyorForm()
        formset = ClmDocForm(queryset=XxgenClaimsDocs.objects.none())


    context['claimSurveyForm'] = claimSurveyForm
    context['formset'] = formset


    return render(request, 'Claims/Claim_Surveyor_Process.html', context)


def process_pending_claims(request,**kwargs):
    context = {}

    claimid = kwargs.get("claim_id")

    ClmPaymentForm = CalimsPaymentsForm(request.POST or None)

    if not XxgenClaimsPayments.objects.filter(claim=claimid).exists():
        obj = XxgenClaimsProcessDtls.objects.get(claim=claimid)
        XxgenClaimsPayments.objects.create(payment_receipt_id=XxgenClaimsPayments.objects.count()+1,
                                              claim = XxgenClaims.objects.get(claim_id=claimid),
                                           amount_piad = obj.amount_setteled)

    if request.method == "GET":
        try:
            sinst = XxgenClaimsPayments.objects.get(claim=claimid)
            ClmPaymentForm = CalimsPaymentsForm(instance=sinst)
        except XxgenClaimsPayments.DoesNotExist:
            ClmPaymentForm = CalimsPaymentsForm()

    if request.method == "POST":
        sinst = XxgenClaimsPayments.objects.get(claim=claimid)
        ClmPaymentForm = CalimsPaymentsForm(request.POST,instance=sinst)

        if ClmPaymentForm.is_valid():
            payment = ClmPaymentForm.save(commit=False)
            payment.created_by = str(request.user)
            payment.last_updated_by = str(request.user)
            payment.save()

            obj, created = XxgenClaims.objects.update_or_create(
                claim_id=claimid,
                defaults={'claim_status': 'CLOSED'})

            obj, created = XxgenClaimsProcessDtls.objects.update_or_create(
                claim=claimid,
                defaults={'claim_status': 'CLOSED'}
            )
            context['message'] = "Payment Processed Successfully...."

    context['ClmPaymentForm'] = ClmPaymentForm

    return render(request, 'Claims/Claim_Payment_Process.html', context)

