from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def index(request):
    now = datetime.now()
    return render(request, "newyear/index.html", {
        "is_newyear": now.month == 1 and now.day == 1
        # "is_newyear": True
    })