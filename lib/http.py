import json
from django.http import HttpResponse
from swiper import settings

def render_json(data,code=0):
    json_dict = {
        'data':data,
        'code':code,
    }
    if settings.DEBUG:
        result = json.dumps(json_dict, ensure_ascii=False,indent=4,sort_keys=True)

    else:
        result = json.dumps(json_dict,  separators=[',', ':'])
    return HttpResponse(result, content_type='application/json;charset=UTF-8')