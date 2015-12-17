# coding: utf-8
import json

from Gitpard.apps.analysis import helpers
from django.utils import timezone
from rest_framework import serializers
import models
from rest_framework.exceptions import ValidationError


class ReportSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data.update({
            'user': self.context['request'].user,
            'repository': self.context["repository"],
            'state': models.Report.PREPARED,
            'path': helpers.create_report_path(),
            'datetime': timezone.now(),
            'report': json.dumps([])
        })
        return super(ReportSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        pass

    def validate_mask(self, mask):
        mask_obj = json.loads(mask)
        try:
            assert "include" in mask_obj
            assert isinstance(mask_obj["include"], list)
            assert "exclude" in mask_obj
            assert isinstance(mask_obj["exclude"], list)
        except AssertionError:
            raise ValidationError(u"Bad request. Wrong mask format")
        return mask

    class Meta:
        model = models.Report
        fields = ('id', 'user', 'repository', 'branch', 'datetime', 'kind', 'state', 'mask', 'report', 'path')
        read_only_fields = ('id', 'user', 'repository', 'state', 'datetime', 'report', 'path')