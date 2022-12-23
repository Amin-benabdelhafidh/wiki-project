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
    edit = forms.BooleanField(initial=False,widget=forms.HiddenInput())



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
    # check request method
    if request.method == 'POST':
        form = NewPageform(request.POST)
        # check validation
        if form.is_valid():
            # get data
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            edit = form.cleaned_data['edit']

            if edit is False:
                if util.get_entry(title) is None:
                    util.save_entry(title, text)
                    return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            elif edit is True:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            else:
                 return render(request, 'encyclopedia/newpage.html', {
                    "form": form,
                    "title": title,
                    "filexists": True,
                    "message": 'this title already exists!'
                })

        else:
            return render(request, 'encyclopedia/newpage.html', {
                "form": form
            })
    # render the form
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageform(),
            "filexists": False,
            "n": True
        })

def edit(request, entry):
    page = util.get_entry(entry)
    if page == None:
        return render(request, "encyclopedia\error404.html", {
            "notfound": True,
            "entry": entry
        })
    
    else:
        form = NewPageform()
        form['title'].initial = entry
        form['text'].initial = page
        form['edit'].initial = True
        return render(request, "encyclopedia/newpage.html", {
            'form': form,
            'n': False
        })


def random(request):
    l = util.list_entries()
    s = len(l)
    x = randint(0, s - 1)
    for i in range(s):
        if x == i:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': l[i]}))
    return render(request, "encyclopedia/error404.html")

        