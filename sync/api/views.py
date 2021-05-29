import json
import random

from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.serializers import UploadSerializer, GetSumSerializer


class SetArray(GenericAPIView):
    """Set  json file  with 'Array' key in dict"""
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def post(self, request, format=None):
        """
        Return answer.
        """
        # print(request.data)
        # print('session', request.session.keys(), request.session.items(), request.session.session_key)
        # print(dir(request.session))
        upload = self.get_serializer(data=request.data, )
        # print(upload)

        # num_visits = request.session.get('num_visits', 0)
        # print(num_visits)
        # request.session['num_visits'] = num_visits + 1

        if upload.is_valid():
            file = upload.validated_data['file']
            x = file.read()
            nums = json.loads(x)['array']
            # print(nums)
            result_sum = self.calculate_sum(nums)
            result_id = random.randint(0, 10000)
            resp = {'ID': result_id, 'SUM': result_sum}
            request.session['ID'] = result_id
            request.session['sum'] = result_sum
            return Response(resp)

        return Response({"Failure": "Error"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def calculate_sum(nums):
        """"""
        # если встречаются значения с точкой, запятой - приводим к общему виду float
        buf = []
        for i in nums:
            if i is None:
                continue
            buf.append(i.replace(',', '.'))
        # проверяем тип, суммируем
        result = 0
        for n in buf:
            f = float(n)
            try:
                if isinstance(f, float):
                    result += f
            except ValueError as ex:
                print(f'for log: {ex}')
                continue
        return result


class GetSum(GenericAPIView):
    """Getting result"""
    serializer_class = GetSumSerializer

    def post(self, request, format=None):
        serializer = GetSumSerializer(data=request.data)
        if serializer.is_valid():
            request_data = serializer.validated_data

            # -----  если есть уже расситанный в куках реквеста с совпадающим ID (повторное обращение за данными)------
            if {'ID', 'sum'}.issubset(request.session.keys()) and request.session['ID'] == request_data['ID']:
                resp = {'SUM': request.session['sum']}
                return Response(resp, status=status.HTTP_200_OK)

            # -----  если сессия реквеста не та или нету, но запрос по ID, то ищем sum в бд - модели session------

            for i in Session.objects.all():
                s_data = i.get_decoded()
                # print('session_i', s_data)
                if 'ID' in s_data and request_data['ID'] == s_data['ID']:
                    resp = {'SUM': i.get_decoded()['sum']}

                    return Response(resp, status=status.HTTP_200_OK)
            else:
                resp = {'Failure': 'ID not found. If you want to get SUM, send json file to ../api/v1/set/ endpoint'}

                return Response(resp, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
