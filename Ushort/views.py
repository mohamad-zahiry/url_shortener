from django.shortcuts import render


def home(request):
    return render(request, "Ushort/home.html", {})
