from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['JSON', ], ), ])

    class Meta:
        fields = ['file']


class GetSumSerializer(serializers.Serializer):
    ID = serializers.IntegerField()

    class Meta:
        fields = ['ID']
