# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Auto-login after signup
#             return redirect('home')  # Change 'home' to your actual homepage route name
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Or wherever
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
