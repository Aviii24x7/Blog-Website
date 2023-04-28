from django.shortcuts import render,get_object_or_404
from .models import Post,Author,Tag
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views import View
from django.urls import reverse

# from datetime import date
from .forms import CommentForm

# all_posts = [
# ]
#helper function
# def get_date(post):
    # return post['date']

# Create your views here.
class StartingPageView(ListView):
    template_name="aviBlog/home.html"
    model=Post
    ordering=["-date"]
    context_object_name="the_posts"

    def get_queryset(self):
        queryset= super().get_queryset()
        data=queryset[:3]
        return data

# def homeview(request):

#     latest_posts= Post.objects.all().order_by("-date")[:3]
#     return render(request, "aviBlog/home.html", {"the_posts":latest_posts} )
    # sorted_posts=sorted(all_posts, key=get_date)
    # latest_posts=sorted_posts[-2:]
 
class AllPostsView(ListView):
    template_name="aviBlog/postfeed.html"
    model=Post
    ordering=["-date"]
    context_object_name="all_posts"

# def posts(request):
#     all_posts=Post.objects.all().order_by("-date")
#     return render(request,'aviBlog/postfeed.html', {"all_posts":all_posts})

class SinglePostView(View):
    #template_name="aviBlog/postdetail.html"
    #model=Post
    def is_stored_post(self, request, post_id):
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later=post_id in stored_posts
        else:
            is_saved_for_later=False

        return is_saved_for_later

    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request, post.id)
        }
        return render(request,"aviBlog/postdetail.html", context)
    
    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post=post
            comment.save()            
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request, post.id)
        }
        return render(request,"aviBlog/postdetail.html", context)
        

class ReadLaterView(View):

    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        
        if stored_posts is None or len(stored_posts)==0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            # posts = Post.objects.all()
            context["posts"] = posts
            context["has_posts"] = True 
            
        return render(request,"aviBlog/storedposts.html", context)
        
    
    
    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        
        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])
        # post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
    # Without Comment
    # def get_context_data(self, **kwargs):
    #     context= super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"]=CommentForm()
    #     return context

# def post_slug(request,slug):
#     # identified_post=next(post for post in all_posts if post['slug']==slug)

#     # identified_post=Post.objects.get(slug=slug)
#     identified_post=get_object_or_404(Post,slug=slug)


#     return render(request, "aviBlog/postdetail.html", {"post":identified_post,
                                                    #    "post_tags":Tag.objects.all()})