import json

import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from main.utils.my_utils import MyUtil

u = MyUtil()

class AddressViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        curl --location --request GET 'http://localhost:8003/api/addresses?input=22Elmavenue'
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        _id = u.save_request(
            input=json.dumps(request.GET),
            ip=request.META.get('HTTP_X_FORWARDED_FOR') or "127.0.0.1"
        )
        input = request.GET.get("input")
        if input is None:
            return Response({
                "code": 400,
                "message": "input not provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        input = input.replace(" ", "%20")
        print(input)
        url = f"{settings.GOOGLE_MAP_BASE_URL}/place/autocomplete/json?input={input}&key={settings.GOOGLE_MAP_KEY}&types=address&components=country:za"
        resp = requests.get(url=url, headers={"Content-Type": "application/json"})
        r = list()
        # print(url)
        if resp.status_code == 200:
            # print(resp.json())
            for item in resp.json()["predictions"]:
                r.append({"address": item["description"], "id": item["place_id"]})
                # print(item.__dict__)
        _resp = {
            "code": 200,
            "input": input,
            "addresses": r
        }
        u.save_response(
            id=_id,
            output=json.dumps(_resp),
            response_code=_resp["code"]
        )
        return Response(_resp, status=status.HTTP_200_OK)