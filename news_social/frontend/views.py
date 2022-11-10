from django.shortcuts import render
# from frontend.user.html_files import


def signup(request):
    # render function takes argument  - request
    # and return HTML as response
    return render(request, "signup.html")
