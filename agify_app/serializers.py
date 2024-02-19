from rest_framework import serializers

class AgeGuessSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(required=False)
    date_of_birth = serializers.IntegerField(required=False)
