import json

from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework.fields import FileField
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView


def validate_file_size(temp_file):
    print(f'{temp_file=}', 1)
    raise serializers.ValidationError('Пиздец')


def validate_file_type(temp_file):
    print(f'{temp_file=}', 2)
    raise serializers.ValidationError('Пиздец')


class UploadSerializer(Serializer):
    file = FileField(validators=[FileExtensionValidator(allowed_extensions=['json'], code=201, message='неправильный '
                                                                                                       'формат'), ])

    class Meta:
        fields = ['file']


class SumArray(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def post(self, request, format=None):
        file = request.FILES.get('file')
        x = file.read()
        print(json.loads(x))
        resp = {'Hello kitty': 'OK'}
        return Response(resp)

    def check(self):
        """"""
        pass
