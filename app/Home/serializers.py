from rest_framework import serializers
from .models import contact_form

class contact_form_serializer(serializers.ModelSerializer):
    class Meta:
        model=contact_form
        fields='__all__'