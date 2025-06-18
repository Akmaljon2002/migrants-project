from rest_framework import serializers


class ChartItemSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.IntegerField()


class ChartResponseSerializer(serializers.Serializer):
    title = serializers.CharField()
    data = ChartItemSerializer(many=True)