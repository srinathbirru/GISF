from django.db import models
from datetime import datetime
from django.urls import reverse
# Create your models here.

class XxgenClaims(models.Model):
    claim_id = models.BigIntegerField(primary_key=True)
    policy_no = models.BigIntegerField()
    claim_date = models.DateField(blank=True, null=True)
    claim_risk = models.CharField(max_length=200, blank=True, null=True)
    amount_claimed = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    amount_setteled = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_of_settele = models.DateField(blank=True, null=True)
    total_policy_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_claim_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    claim_status = models.CharField(max_length=200, blank=True, null=True)
    Remarks =  models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.claim_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaims, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Claims1:ProcessClaim1', kwargs={"claim_id": self.claim_id})

class XxgenClaimsDocs(models.Model):
    claim_doc_id = models.AutoField(primary_key=True)
    claim = models.BigIntegerField()
    doc_type_code = models.CharField(max_length=200, blank=True, null=True)
    doc_description = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.claim_doc_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimsDocs, self).save(*args, **kwargs)

class XxgenClaimsProcessDtls(models.Model):
    clm_process_id = models.BigIntegerField(primary_key=True)
    #claim = models.ForeignKey(XxgenClaims, models.DO_NOTHING, blank=True, null=True)
    claim = models.IntegerField()
    policy_no = models.IntegerField()
    claim_date = models.DateField(blank=True, null=True)
    amount_claimed = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    amount_setteled = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_of_settele = models.DateField(blank=True, null=True)
    total_policy_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_claim_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    claim_status = models.CharField(null=True,max_length=120)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.clm_process_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimsProcessDtls, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Claims1:ClaimPay', kwargs={"claim_id": self.claim})

class XxgenClaimsSurveyorDtls(models.Model):
    surveyor = models.ForeignKey('Masters.XxgenClaimsSurveyorMaster', models.DO_NOTHING)
    claim = models.IntegerField()
    clm_survey_status = models.CharField(max_length=200, blank=True, null=True)
    surveyor_comments = models.TextField(null=True)
    surveyor_claim_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('Claims1:SurveyProcess', kwargs={"claim_id": self.claim})


    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimsSurveyorDtls, self).save(*args, **kwargs)


class XxgenClaimsPayments(models.Model):
    payment_receipt_id = models.AutoField(primary_key=True)
    claim = models.ForeignKey(XxgenClaims, models.DO_NOTHING, blank=True, null=True)
    amount_piad = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_of_piad = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.payment_receipt_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimsPayments, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Claims1:ClaimPay', kwargs={"claim_id": self.claim})

