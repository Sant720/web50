from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from random import randint

from . import util

class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'edit_form'}))

    def clean_content(self):
        content = self.cleaned_data["content"]
        if not content.startswith("# "):
            raise forms.ValidationError("Please start your content with a title hashtag (# Title)")
        return content

class CreateForm(forms.Form):
    title = forms.CharField(label="Page Title", max_length=25)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'edit_form', 'placeholder': "# Don't Forget Your Page Title\n\nAnd write some awesome content!"}))
    
    def clean_title(self):
        title = self.cleaned_data["title"]
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            raise forms.ValidationError("A page with this title already exists.")
        return title

    def clean_content(self):
        content = self.cleaned_data["content"]
        if not content.startswith("# "):
            raise forms.ValidationError("Please start your content with a title hashtag (# Title)")
        return content
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    return HttpResponseRedirect(reverse("wiki:index"))

def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": util.markdowner(entry)
    })

def search(request):
    if request.method == "POST":
        q = request.POST['q'].strip()
        matches = []
        for entry in util.list_entries():
            q_low, entry_low = q.lower(), entry.lower()
            if q_low == entry_low:
                return HttpResponseRedirect(reverse("wiki:wiki") + q)
            if q_low in entry_low:
                matches.append(entry)
        return render(request, "encyclopedia/search.html", {
            "q": q,
            "matches": matches
        })
    return HttpResponseRedirect(reverse("wiki:index"))

def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = "".join([line for line in form.cleaned_data["content"] if line != "\n"])
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("wiki:wiki") + entry) 
        return render(request, "encyclopedia/edit.html", {
            "edit_form": form
        })

    content_body = util.get_entry(entry)
    if not content_body:
        return render(request, "encyclopedia/search.html", {
            "q": entry, 
            "matches": None
        })
    content = {'content': content_body}
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "edit_form": EditForm(initial=content)
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            lines = "".join([line for line in content if line != "\n"])
            util.save_entry(title, lines)
            return HttpResponseRedirect(reverse("wiki:wiki") + title)
        return render(request, "encyclopedia/create.html", {
            "create_form": form
        })
        
    return render(request, "encyclopedia/create.html", {
        "create_form": CreateForm()
    })

def random(request):
    ls = util.list_entries()
    page = ls[randint(0, len(ls) - 1)]
    return HttpResponseRedirect(reverse("wiki:wiki") + page)