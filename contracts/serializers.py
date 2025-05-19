from rest_framework import serializers
from .models import Contract, Supplier, Buyer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    buyer = BuyerSerializer()

    class Meta:
        model = Contract
        fields = '__all__'