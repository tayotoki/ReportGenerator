from rest_framework import serializers

from request.models import Request


class RequestStatsSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source="state.name")
    status_name = serializers.ReadOnlyField(source="status.name")

    class Meta:
        model = Request
        fields = [field.name for field in model._meta.fields] + ["status_name", "state_name"]
        read_only_fields = fields
