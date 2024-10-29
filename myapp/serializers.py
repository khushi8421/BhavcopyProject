from rest_framework import serializers
from .models import EquityRecord

class EquityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquityRecord
        fields = [
            'code',    
            'name',    
            'open',    
            'high',    
            'low',     
            'close',   
        ]
