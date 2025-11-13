from rest_framework import serializers


class SaplingsCalculatorSerializer(serializers.Serializer):
	count = serializers.IntegerField(min_value = 0)
