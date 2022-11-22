from django.shortcuts import render
# from frontend.user.html_files import


def signup(request):
    # render function takes argument  - request
    # and return HTML as response
    context_data = {}
    return render(request, "signup.html", context=context_data)


def index_view(request):
    context_data = {}
    return render(request, "index.html", context=context_data)
