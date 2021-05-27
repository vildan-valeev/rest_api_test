import json

from django.core.validators import FileExtensionValidator
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['JSON',], ), ])
    class Meta:
        fields = ['file']


class SumArray(GenericAPIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def post(self, request, format=None):
        """
        Return answer.
        """
        print(request.data)
        # upload = UploadSerializer(data=request.FILES['file'])
        # self.get_s
        upload = self.get_serializer(data=request.data,)
        print(upload)
        # print(upload)
        print(upload.is_valid())
        if upload.is_valid():
            file = upload.validated_data['file']
            x = file.read()
            nums = json.loads(x)['array']
            print(nums)
            resp = {'Sum': self.get_sum(nums)}
            return Response(resp)

        return Response({"Failure": "Error"}, status=status.HTTP_400_BAD_REQUEST)


    def get_sum(self, nums):
        """"""
        # если встречаются значения с точкой, запятой - приводим к общему виду float
        print(nums)
        buf = []
        for i in nums:
            if i is None:
                continue
            buf.append(i.replace(',', '.'))
        # проверяем тип, суммируем
        sum = 0
        for n in buf:
            f = float(n)
            try:
                if isinstance(f, float):
                   sum += f
            except ValueError as ex:
                continue
        return sum
