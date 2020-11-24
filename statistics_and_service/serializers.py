from rest_framework import serializers

class data_to_real_estate_website_Serializer(serializers.Serializer):
    input_values=serializers.JSONField()