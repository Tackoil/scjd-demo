import json

from django.http import HttpResponse


def patent_pie(request):
    if request.method == 'GET':
        res = {
            "num_patent_types": [84, 901, 52],
            "num_applicants_types": [262, 546, 134, 55, 40],
          }
        res = json.dumps(res)
        return HttpResponse(res)

