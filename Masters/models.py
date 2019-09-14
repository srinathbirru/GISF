from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.conf import settings
from django.urls import reverse

# Create your models here.
class XxgenAgenMaster(models.Model):
    agen_id = models.CharField(primary_key=True, max_length=120)
    agent_name = models.CharField(max_length=200, blank=True, null=True)
    agent_dob = models.DateField(blank=True, null=True)
    agent_age = models.IntegerField(blank=True, null=True)
    agent_qualification = models.CharField(max_length=50, blank=True, null=True)
    agent_join_date = models.DateField(blank=True, null=True, auto_now_add=True,)
    agent_start_date = models.DateField(blank=True, null=True)
    agent_end_date = models.DateField(blank=True, null=True)
    agent_status = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True).hidden
    created_date = models.DateField(blank=True, null=True, auto_now_add=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True).hidden
    last_update_date = models.DateField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return str(self.agen_id)


    def get_agent_age(self):
        import datetime
        return int(((datetime.date.today() - self.agent_dob).days / 365.25))

    def get_unique_id(self):
        a = self.agent_name[:2].upper()  # First 2 letters of last name
        b = self.agent_dob.strftime('%d')  # Day of the month as string
        c = self.agent_qualification[:2].upper()  # First 2 letters of city
        d = 'AG-'
        return d + a + b + c

    def save(self, *args, **kwargs):
        print('get_unique_id',self.get_unique_id())
        #self.agen_id= self.get_unique_id()
        self.agent_age = self.get_agent_age()
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenAgenMaster, self).save(*args, **kwargs)

class XxgenProductMaster(models.Model):
    prod_code = models.CharField(primary_key=True, max_length=200)
    prod_description = models.CharField(max_length=2000, blank=True, null=True)
    prod_start_date = models.DateField(blank=True, null=True)
    prod_end_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)

    def save(self):
        if not self.prod_code:
            self.created_date = datetime.today()
            self.last_update_date = datetime.today()
        super(XxgenProductMaster, self).save()

    def __str__(self):
        return self.prod_code

class XxgenProductRiskMaster(models.Model):

    risk_code = models.CharField(primary_key=True, max_length=200)
    prod_code = models.ForeignKey(XxgenProductMaster, models.DO_NOTHING, db_column='prod_code', blank=True, null=True)
    risk_description = models.CharField(max_length=2000, blank=True, null=True)
    risk_premium_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    risk_start_date = models.DateField(blank=True, null=True)
    risk_end_date = models.DateField(blank=True, null=True)
    prem_calc_method = models.CharField(max_length=200, blank=True, null=True)
    fixed_prem = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fixed_si = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.risk_code

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenProductRiskMaster, self).save(*args, **kwargs)

class Xxgen_agent_Prod_Comm_Master(models.Model):
    agen_id = models.ForeignKey('XxgenAgenMaster', models.DO_NOTHING, blank=False, null=False )
    prod_code = models.ForeignKey('XxgenProductMaster', models.DO_NOTHING, db_column='prod_code', blank=True, null=True)
    comm_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.prod_code

    def save(self):
        if not self.agen_id:
            self.created_date = datetime.today()
            self.last_update_date = datetime.today()
        super(Xxgen_agent_Prod_Comm_Master, self).save()


class XxgenVehicleMaster(models.Model):
    class Meta:
        unique_together = (('mfg_company_name', 'model_id','model_name'),)

    mfg_company_name = models.CharField(max_length=200, blank=True, null=True)
    model_id = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200, blank=True, null=True)
    engine_cubic_capacity = models.CharField(max_length=200, blank=True, null=True)
    insured_declared_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True, default=datetime.now)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True, )
    last_update_date = models.DateField(blank=True, null=True, default=datetime.now)

    def __str__(self):
        return self.model_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenVehicleMaster, self).save(*args, **kwargs)


class XxgenVehicleDepriciation(models.Model):
    vehicle_age_from = models.IntegerField(blank=True, null=True)
    vehicle_age_to = models.IntegerField(blank=True, null=True)
    dep_percent_on_idv = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenVehicleDepriciation, self).save(*args, **kwargs)

class XxgenNcbMaster(models.Model):
    prod_code = models.ForeignKey('XxgenProductMaster', models.DO_NOTHING, db_column='prod_code', blank=True, null=True)
    no_years_from = models.BigIntegerField(blank=True, null=True)
    no_years_to = models.BigIntegerField(blank=True, null=True)
    discount_on_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_desc = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenNcbMaster, self).save(*args, **kwargs)

class XxgenClaimStatusMaster(models.Model):
    clm_status_code = models.CharField(unique=True, max_length=200)
    clm_status_desc = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.clm_status_code

    def get_absolute_url(self):
        return reverse('MasterSetup:claimStatusMaster', kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimStatusMaster, self).save(*args, **kwargs)

class XxgenClaimsSurveyorMaster(models.Model):
    surveyor_id = models.IntegerField(primary_key=True)
    surveyor_name = models.CharField(max_length=200, blank=True, null=True)
    surveyor_qualificaition = models.CharField(max_length=200, blank=True, null=True)
    surveyor_brach_code = models.CharField(max_length=200, blank=True, null=True)
    surveyor_city = models.CharField(max_length=200, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    last_updated_by = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
        return self.surveyor_id

    def save(self, *args, **kwargs):
        self.created_date = datetime.today()
        self.last_update_date = datetime.today()
        super(XxgenClaimsSurveyorMaster, self).save(*args, **kwargs)
