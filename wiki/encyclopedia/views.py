from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util
from markdown2 import Markdown

class NewEntry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"title":"Title"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"name":"Content"}))
    
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikipage(request, page):
    pages = [page.lower() for page in util.list_entries()]
    # BAD REQUEST, NO PAGE WITH CONTENT
    if page.lower() not in pages:
        content = "No data about this entrie."
        return HttpResponseRedirect("/error")
    # page exists, set content and render
    content = util.get_entry(page.lower())
    markdown = Markdown()
    markdown = markdown.convert(content)
    return render(request, "encyclopedia/wikipage.html", {
                                                        "title": page,
                                                        "content": markdown
                                                        })
                                        

def random(request):
    pages = [page.lower() for page in util.list_entries()]
    from random import choice
    page = choice(pages)
    return HttpResponseRedirect(f"/wiki/{page}")
    
    
def search(request):
    if "q" not in request.GET:
        return HttpResponseRedirect("")
    
    if "q" in request.GET:
        page = request.GET["q"]
        pages = [page.lower() for page in util.list_entries()]
    
    if page.lower() in pages:
        return HttpResponseRedirect(f"wiki/{page}")
    
    from re import search, IGNORECASE
    content = []
    for p in pages:
        if search(page, p, IGNORECASE):
            content.append(p)
    return render(request, "encyclopedia/search.html", {
                                                        "title": "Search results",
                                                        "content": content
                                                        })
                                                        

def newentry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html", {
                                                        "title": "New entry",
                                                        "form": NewEntry()
                                                        })

    form = NewEntry(request.POST)
    if not form.is_valid():
        return render(request, "encyclopedia/newentry.html", {
                                                            "title": "New entry",
                                                            "form": form
                                                            })

    title = form.cleaned_data["title"].lower()
    content = form.cleaned_data["content"]
    if title.lower() in util.list_entries():
        return render(request, "encyclopedia/newentry.html", { "title": "404", "content": "We already have page with this title. Please use edit function or change title.", "form": form })
    else:
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{title}")
        
def error(request):
    return render(request, "encyclopedia/error.html", {"title": "404", "content": "Requested page was not found."})
    
    
def edit(request, page):
    if request.method == "GET":
        content = util.get_entry(page)
        data = {"title": page, "content": content}
        return render(request, "encyclopedia/edit.html", {
                                                        "title": f"Edit {page}",
                                                        "form": NewEntry(data)
                                                        })

    data = NewEntry(request.POST)
    if not data.is_valid():
        return render(request, "encyclopedia/edit.html", {
                                                    "title": f"Edit {page}",
                                                    "form": NewEntry(data)
                                                    })
    title = data.cleaned_data["title"]
    content = data.cleaned_data["content"]
    util.save_entry(title, content)
    return HttpResponseRedirect(f"/wiki/{title}")
