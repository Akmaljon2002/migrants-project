from rest_framework import serializers
from apps.migrant.models import Migrant


class MigrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Migrant
        fields = '__all__'
