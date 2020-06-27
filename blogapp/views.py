from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home(request):
    posts = [
        {
            "author": "Ahmed Munir",
            "date_posted": "Auguest 20, 2020",
            "title": "Cyber Security",
            "content": "This is my post about cyber security which i hope it is good think."
        },
                {
            "author": "Mahmoud Munir",
            "date_posted": "April 10, 2020",
            "title": "Software development",
            "content": "This is my post about software development which i hope it is good think."
        }
    ]

    context = {
        "posts": posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')