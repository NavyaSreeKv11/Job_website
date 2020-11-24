from rest_framework import serializers
from job_easy.models import User, job


class createdjobSerializer(serializers.Serializer):
    input_values = serializers.JSONField()


class createdApplicationSerializer(serializers.Serializer):
    input_values = serializers.JSONField()


class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class jobsSerializer(serializers.ModelSerializer):
    user = getUserSerializer()

    class Meta:
        model = job
        fields = "__all__"
