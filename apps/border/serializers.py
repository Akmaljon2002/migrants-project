from rest_framework import serializers
from apps.border.models import BorderCross


class BorderCrossSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorderCross
        fields = '__all__'