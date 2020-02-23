from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.
def index(req):
    myposts = Blogpost.objects.all()
    print(myposts)
    return render(req,'blog/index.html',{'myposts':myposts})

def blogpost(req, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    print(post)
    return render(req,'blog/blogpost.html',{'post':post})
