from django.db import models

# Create your models here.

class AgeGuess(models.Model):
    name = models.CharField(max_length=256, default="")
    age = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " ("+ str(self.age)+ ")"
