from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Language, Exercise, UserProgress
#from .serializers import ExerciseSerializer, LeaderboardSerializer
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')


def home(request):
    available_languages = Language.objects.all()
    selected_language = None  # Initialize selected_language
    if request.method == 'POST':
        selected_language_id = request.POST.get('language_id')
        try:
            selected_language = Language.objects.get(id=selected_language_id)
        except Language.DoesNotExist:
            # Handle the case where the selected language does not exist
            pass

    context = {'available_languages': available_languages, 'selected_language': selected_language}
    return render(request, 'home.html', context)


def calculate_score(exercises, user_responses):
    score = 0
    total_possible_score = 0  # To calculate proficiency level
    for exercise in exercises:
        total_possible_score += exercise.difficulty

        correct_choice = exercise.correct_choice
        user_choice = user_responses.get(f'question_{exercise.id}')

        if user_choice == correct_choice:
            score += exercise.difficulty  # You may adjust scoring logic as needed

    proficiency_percentage = (score / total_possible_score) * 100
    proficiency_level = calculate_proficiency_level(proficiency_percentage)
    return score, proficiency_level

def calculate_proficiency_level(proficiency_percentage):
    if proficiency_percentage >= 90:
        return 'Advanced'
    elif proficiency_percentage >= 70:
        return 'Intermediate'
    elif proficiency_percentage >= 50:
        return 'Beginner'
    else:
        return 'Novice'

def save_user_progress(user, language, score, exercises, proficiency_level):
    user_progress, created = UserProgress.objects.get_or_create(user=user, language=language)
    user_progress.score += score
    user_progress.proficiency_level = proficiency_level
    user_progress.save()

def score_page(request):
    user_progress = UserProgress.objects.get(user=request.user)  # Assuming only one UserProgress per user
    context = {'score': user_progress.score}
    return render(request, 'score_page.html', context)

@login_required
def exercises(request, language_id):
    try:
        language = Language.objects.get(id=language_id)

        # Get or create user progress for the selected language
        user_progress, created = UserProgress.objects.get_or_create(user=request.user, language=language)

        exercises = Exercise.objects.filter(language=language)

        # Determine user performance level and adjust difficulty of questions
        difficulty_threshold = 3  # Adjust as needed
        if user_progress.score >= difficulty_threshold:
            exercises = exercises.filter(difficulty__gte=difficulty_threshold)
        else:
            exercises = exercises.filter(difficulty__lt=difficulty_threshold)

        # Limit the number of questions displayed
        exercises = exercises[:10]  # Adjust the number of questions as needed

    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

    if request.method == 'POST':
        user_responses = request.POST  # Assuming the form uses POST method
        score, proficiency_level = calculate_score(exercises, user_responses)
        save_user_progress(request.user, language, score, exercises, proficiency_level)

        # Redirect to the score page with proficiency level
        return redirect('score_page')

    context = {'language': language, 'exercises': exercises}
    return render(request, 'exercises.html', context)

@login_required
def user_profile(request):
    user_progress = UserProgress.objects.filter(user=request.user)
    context = {'user_progress': user_progress}
    return render(request, 'user_profile.html', context)

@login_required
def user_settings(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # Assuming you have a form field named 'action'

        if action == 'reset_progress':
            UserProgress.objects.filter(user=request.user).delete()
            messages.success(request, 'Progress reset successfully!')
            return redirect('user_profile')

        # Add other actions as needed

    return render(request, 'user_settings.html')

@login_required
def leaderboard(request, language_id):
    try:
        leaderboard_data = UserProgress.objects.filter(language_id=language_id).order_by('-score')[:10]
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

    # Format leaderboard_data directly
    formatted_leaderboard = [
        {'user_username': entry.user.username, 'user_email': entry.user.email, 'score': entry.score, 'proficiency_level': entry.proficiency_level}
        for entry in leaderboard_data
    ]

    context = {'leaderboard': formatted_leaderboard}
    return render(request, 'leaderboard.html', context)
