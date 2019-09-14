from Masters.models import XxgenProductRiskMaster,XxgenVehicleMaster,XxgenVehicleDepriciation
import datetime

def motor_Risk_prem_calc(mycode,vehicle_year,make,model_id,model_name):
    now = datetime.datetime.now()
    curyear = now.year
    obj = XxgenProductRiskMaster.objects.get(risk_code=mycode)
    risk_desc = obj.risk_description
    if obj.prem_calc_method == 'F':
        risk_prem = obj.fixed_prem
        risk_sa = obj.fixed_si
    if obj.prem_calc_method == 'P':

        vobj = XxgenVehicleMaster.objects.get(mfg_company_name=make,model_id=model_id,model_name=model_name)
        vehicle_age = curyear - vehicle_year
        vdep = XxgenVehicleDepriciation.objects.get(vehicle_age_from=vehicle_age)
        vehicle_dep_percet = vdep.dep_percent_on_idv
        vehicle_dep_value = (vobj.insured_declared_value*vehicle_dep_percet)/100
        vehicle_currrent_value = vobj.insured_declared_value-vehicle_dep_value
        risk_prem = (vehicle_currrent_value*obj.risk_premium_percent)/100
        risk_sa = vehicle_currrent_value
    return risk_desc,risk_sa, risk_prem

def ProRate_prem_calc(risk_prem_per_year,policy_end_date):
    from datetime import date
    now = date.today()
    print('policy_start_date', policy_end_date)
    per_day_prem = risk_prem_per_year/365
    print('per_day_prem',per_day_prem)
    print('cur date',now)
    no_of_days_risk_cover = (policy_end_date-now).days
    print('no_of_days_risk_cover',no_of_days_risk_cover)
    return per_day_prem*no_of_days_risk_cover

