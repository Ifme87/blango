from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm
import logging
#from django.views.decorators.cache import cache_page
#from django.views.decorators.vary import vary_on_cookie
#from django.views.decorators.vary import vary_on_headers
from django.urls import reverse

logger = logging.getLogger(__name__)

# Create your views here.

#@cache_page(300)
#@vary_on_cookie                            #to have effect of different caches for different user sessions
    #or @vary_on_headers("Cookie")
def index(request):
#    from django.http import HttpResponse
#    logger.debug("no cache")               #shouldn't be executed if cached
#    return HttpResponse(str(request.user).encode("ascii"))
    posts = (
        Post.objects.filter(published_at__lte=timezone.now())
        .select_related("author") #- used for optimizing SQL quieries, for ForeignKey in model
        #.defer("created_at", "modified_at") - values of these columns will be missed
        #.only("...", "...") - values of these columns only will be fetched
    )
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )


def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])


def post_table(request):
    return render(
        request, "blog/post-table.html", {"post_list_url": reverse("post-list")}
    )