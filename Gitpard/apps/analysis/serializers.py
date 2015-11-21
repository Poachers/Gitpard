from django.utils import timezone
from rest_framework import serializers
import models


class ReportSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = models.Report
        fields = ('id', 'repository', 'branch', 'datetime', 'kind', 'state', 'mask', 'report')
        read_only_fields = ('id', 'repository', 'datetime', 'report')