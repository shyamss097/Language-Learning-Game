from django.contrib import admin
from .models import Language, Exercise, UserProgress

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'question', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_choice')
    list_filter = ['language']
    search_fields = ['question']

class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'language', 'score', 'proficiency_level')
    list_filter = ['language']
    search_fields = ['user__username']

admin.site.register(Language, LanguageAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
