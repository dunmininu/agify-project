from django.urls import path
from .views import GuessAgeView

urlpatterns = [
    path('human-age', GuessAgeView.as_view(), name='guess-age'),
]
