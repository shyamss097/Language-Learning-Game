# from rest_framework import serializers
# from .models import Exercise, UserProgress
# from django.core.exceptions import FieldDoesNotExist

# class ExerciseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exercise
#         fields = '__all__'



# class LeaderboardSerializer(serializers.ModelSerializer):
#     user_username = serializers.ReadOnlyField(source='user.username')
#     user_email = serializers.ReadOnlyField(source='user.email')

#     class Meta:
#         model = UserProgress
#         fields = '__all__'
