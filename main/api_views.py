import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response


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
        return Response({
            "code": 200,
            "input": input,
            "addresses": r
        }, status=status.HTTP_200_OK)