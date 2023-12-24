from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    question = models.TextField()
    difficulty = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    choice_a = models.CharField(max_length=255, null=True)
    choice_b = models.CharField(max_length=255, null=True)
    choice_c = models.CharField(max_length=255, null=True)
    choice_d = models.CharField(max_length=255, null=True)
    correct_choice = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"{self.language.name} - Exercise {self.id}: {self.question[:20]}..."

class UserProgress(models.Model):
    NOVICE = 'Novice'
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    PROFICIENCY_LEVEL_CHOICES = [
        (NOVICE, 'Novice'),
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL_CHOICES, default=NOVICE)

    def __str__(self):
        return f"{self.user.username} - {self.language.name} - Score: {self.score}, Proficiency Level: {self.proficiency_level}"
