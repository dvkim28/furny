from rest_framework import serializers


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'category']