from .models import XxgenPolicyBills,XxgenPolicyDtls
def Generate_invoice(policy_no,premium_amount,submit_user):

    obj = XxgenPolicyDtls.objects.get(policy_no=policy_no)

    XxgenPolicyBills.objects.create(policy_no=policy_no,
                                    premium_amount=premium_amount,
                                    created_by=str(submit_user),
                                    last_updated_by=str(submit_user),
                                    bill_id=XxgenPolicyBills.objects.count()+1
                                    )