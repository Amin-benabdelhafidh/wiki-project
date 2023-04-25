from django.shortcuts import render
from django import forms
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randint
from . import util

class NewPageform(forms.Form):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Title...'}))
    text = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Enter your text...'}))

class EditPageform(forms.Form):
    text = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Enter your text...'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })


def entry(request, entry):
    mark = Markdown()
    page = util.get_entry(entry)
    
    if page == None:
        return render(request, "encyclopedia/error404.html", {
            "title": entry
        })
    else:
        cont = mark.convert(page)
        return render(request, "encyclopedia/page.html", {
            "content": cont,
            "title": entry
        })


def notfound(request, entry):
    return render(request, "encyclopedia\error404.html", {
        "notfound": True,
        "page": entry
    })


def search(request):
    # get request with 'POST' method
    title = request.POST.get('q', '')
    # redirect user
    if util.get_entry(title) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
    # if title doesn't match return list of titles that may be close 
    else:
        titles = []
        for i in util.list_entries():
            if title.lower() in i.lower():
                titles.append(i)

        if len(titles) == 0:
            return HttpResponseRedirect(reverse("notfound", kwargs={"entry": title}))

    return render(request, "encyclopedia/index.html", {
        "title": titles
    })


def newpage(request):
    if request.method == 'POST':
        form = NewPageform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['text']
            if util.get_entry(title) == None:
                util.save_entry(title, content)
            else:
                return render(request, "encyclopedia/newpage.html", {
                    'msg': True,
                    'title': title,
                })

            return HttpResponseRedirect(f"wiki/{title}")
    else:
        form = NewPageform()
    return render(request, "encyclopedia/newpage.html", {
        "form": form,
    })
    

def edit(request, entry):
    if request.method == "POST":
        form = EditPageform(request.POST)
        if form.is_valid():
            util.save_entry(entry, form.cleaned_data["text"])
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": entry}))
    else:
        page = util.get_entry(entry)
        form = EditPageform()
        form.fields['text'].initial = page
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": entry,
        })
    
    
        


def random(request):
    l = util.list_entries()
    s = len(l)
    try:
        x = randint(0, s - 1)
    except ValueError:
        return render(request, "encyclopedia/error404.html")
    for i in range(s):
        if x == i:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': l[i]}))
    return render(request, "encyclopedia/error404.html")

        