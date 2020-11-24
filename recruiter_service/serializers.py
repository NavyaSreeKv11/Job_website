from rest_framework import serializers

class recruiter_Serializer(serializers.Serializer):
    input_values=serializers.JSONField()