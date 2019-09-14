from Masters.models import XxgenProductRiskMaster,XxgenVehicleMaster,XxgenVehicleDepriciation
from django.http import JsonResponse

def get_risk_details(request):
    riskcode = request.GET.get('username', None)
    print('rcode',riskcode)
    if XxgenProductRiskMaster.objects.filter(risk_code='FIRERISK').exists():
        obj = XxgenProductRiskMaster.objects.get(risk_code='FIRERISK')
        data = {
            'is_taken': XxgenProductRiskMaster.objects.filter(risk_code='FIRERISK').exists(),
            'risk_code' : obj.risk_code,
            'risk_desc':obj.risk_description
        }

    data['message']='ndata'

    return JsonResponse(data)