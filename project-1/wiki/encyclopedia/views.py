from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    return HttpResponseRedirect("/")

def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "body": util.markdowner(entry)
    })

