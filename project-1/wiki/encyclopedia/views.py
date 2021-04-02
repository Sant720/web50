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

def search(request):
    if request.method == "POST":
        q = request.POST['q'].strip()
        matches = []
        for entry in util.list_entries():
            q_low, entry_low = q.lower(), entry.lower()
            if q_low == entry_low:
                return HttpResponseRedirect("/wiki/" + q)
            if q_low in entry_low:
                matches.append(entry)
        return render(request, "encyclopedia/search.html", {
            "q": q,
            "matches": matches
        })
    return HttpResponseRedirect("/")
