from datetime import datetime, timedelta
import requests

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AgeGuessSerializer
from .models import AgeGuess

class GuessAgeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AgeGuessSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            cache_key = f"age_{name}"
            cached_response = cache.get(cache_key)

            if not cached_response:
                response = requests.get(f"https://api.agify.io/", params={"name": name})
                if response.status_code == 200:
                    data = response.json()
                    age = data.get('age')
                    year_of_birth = datetime.now().year - age
                    date_of_birth = datetime.now() - timedelta(days=365*age)

                    # Check if an entry already exists
                    age_guess, created = AgeGuess.objects.update_or_create(
                        name=name,
                        defaults={'age': age, 'date_of_birth': date_of_birth.date()}
                    )

                    result = {"name": name, "age": age, "date_of_birth": year_of_birth}
                    cache.set(cache_key, result, timeout=86400)  # Cache for 1 day
                else:
                    return Response({"error": "Failed to fetch data from Agify."}, status=400)
            else:
                result = cached_response

            return Response(result)
        else:
            return Response(serializer.errors, status=400)
