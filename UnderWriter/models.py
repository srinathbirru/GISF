from django.db import models
from datetime import datetime
# Create your models here.

class XxgenInsuredDtls(models.Model):
    insured_id = models.CharField(primary_key=True, max_length=200)
    insured_name = models.CharField(max_length=200, blank=True, null=True)
    insured_dob = models.DateField(blank=True, null=True)
    insured_qualification = models.CharField(max_length=200, blank=True, null=True)
    insured_profission = models.CharField(max_length=200, blank=True, null=True)
    insured_addr_code = models.IntegerField(blank=True, null=True)
    insured_phone = models.BigIntegerField(blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.insured_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenInsuredDtls, self).save(*args, **kwargs)

class XxgenInsuredAddress(models.Model):
    insured_addr_id = models.IntegerField(primary_key=True)
    insured_id = models.ForeignKey(XxgenInsuredDtls, models.DO_NOTHING, db_column='insured_id', blank=True, null=True)
    address_Type = models.CharField(max_length=20, blank=True, null=True)
    insured_addr = models.CharField(max_length=200, blank=True, null=True)
    insured_city = models.CharField(max_length=200, blank=True, null=True)
    insured_state = models.CharField(max_length=200, blank=True, null=True)
    insured_country = models.CharField(max_length=200, blank=True, null=True)
    insured_pincode = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.insured_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenInsuredAddress, self).save(*args, **kwargs)

class XxgenPolicyDtls(models.Model):
    policy_no = models.IntegerField(primary_key=True)
    insured_id = models.ForeignKey('XxgenInsuredDtls', models.DO_NOTHING, db_column='insured_id', blank=True, null=True)
    prod_code = models.ForeignKey('Masters.XxgenProductMaster', models.DO_NOTHING, db_column='prod_code', blank=True, null=True)
    agent_code = models.ForeignKey('Masters.XxgenAgenMaster', models.DO_NOTHING, db_column='agen_id', blank=True, null=True)
    policy_issued_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    policy_status = models.CharField(max_length=200, blank=True, null=True)
    renewal_no = models.BigIntegerField(blank=True, null=True)
    payment_mode = models.CharField(max_length=200, blank=True, null=True)
    total_premium = models.DecimalField(max_digits=20, decimal_places=1, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.policy_no

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenPolicyDtls, self).save(*args, **kwargs)

class XxgenPolicyRiskDtls(models.Model):
    policy_risk_id = models.IntegerField(primary_key=True)
    policy_no = models.ForeignKey(XxgenPolicyDtls, models.DO_NOTHING, db_column='policy_no', blank=True, null=True)
    risk_code = models.ForeignKey('Masters.XxgenProductRiskMaster', models.DO_NOTHING, db_column='risk_code', blank=True, null=True)
    risk_description = models.CharField(max_length=200, blank=True, null=True)
    risk_SA = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    risk_premium = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.risk_code

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenPolicyRiskDtls, self).save(*args, **kwargs)

class XxgenPolicyVehicleDtls(models.Model):
    #policy_no = models.ForeignKey('XxgenPolicyDtls', models.DO_NOTHING, db_column='policy_no', blank=True, null=True)
    policy_no = models.IntegerField(blank=True)
    vehicle_year = models.IntegerField(blank=True, null=True)
    vehicle_make = models.CharField(max_length=200, blank=True, null=True)
    vehicle_model_id = models.CharField(max_length=200, blank=True, null=True)
    vehicle_model_name = models.CharField(max_length=200, blank=True, null=True)
    chasis_number = models.CharField(max_length=200, blank=True, null=True)
    engine_number = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.policy_no

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenPolicyVehicleDtls, self).save(*args, **kwargs)

class XxgenPolicyAgentComm(models.Model):
    #policy_no = models.ForeignKey('XxgenPolicyDtls', models.DO_NOTHING, db_column='policy_no', blank=True, null=True)
    policy_no = models.IntegerField(blank=True)
    agent_id = models.CharField(max_length=120,blank=True, null=True)
    prod_code = models.CharField(max_length=200, blank=True, null=True)
    policy_comm = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.policy_no

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenPolicyAgentComm, self).save(*args, **kwargs)

class XxgenPolicyBills(models.Model):
    bill_id = models.AutoField(primary_key=True)
    #policy_no = models.ForeignKey('XxgenPolicyDtls', models.DO_NOTHING, db_column='policy_no', blank=True, null=True)
    policy_no = models.IntegerField(blank=True)
    premium_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.policy_no

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenPolicyBills, self).save(*args, **kwargs)