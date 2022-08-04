import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm, CreateThreadForm, CreateTagForm
from django.template.defaultfilters import slugify
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# from django.views.decorators.vary import vary_on_headers

logger = logging.getLogger(__name__)

# Create your views here.

# @cache_page(300)
# @vary_on_cookie #(or @vary_on_headers("Cookie")) - to have effect of different caches for different user sessions
def index(request):
    #    logger.debug("no cache")               #shouldn't be executed if cached
    #    return HttpResponse(str(request.user).encode("ascii"))
    posts = (
        Post.objects.filter(published_at__lte=timezone.now()).select_related(
            "author"
        )  # - used for optimizing SQL quieries, for ForeignKey in model
        # .defer("created_at", "modified_at") - values of these columns will be missed
        # .only("...", "...") - values of these columns only will be fetched
    )
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(
                request.POST
            )  # request.POST transfer data of field when its request after sumbit

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                messages.success(request, f"New comment added!")
                logger.info(
                    f"Created comment on Post {post.title} for user {request.user.email}"
                )
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )


def create_post(request):
    if request.user.is_active:
        if request.method == "POST":
            last_form_data = request.POST
            create_form = CreateThreadForm(last_form_data)

            if create_form.is_valid():
                new_post = create_form.save(commit=False)
                new_post.author = request.user
                new_post.slug = slugify(new_post.title)
                new_post.save()
                create_form.save_m2m()  # save m2m after new_post has id, because here we have ManyToManyField
                messages.success(request, f'New thread "{new_post.title}" is created!')
                logger.info(
                    f"Created Post {new_post.title} for user {request.user.username}"
                )
                return redirect("blog:index")
        else:
            create_form = CreateThreadForm()
    else:
        create_form = None
    return render(request, "blog/post-creation.html", {"create_form": create_form})


def create_tag(request):
    if request.user.is_active:
        if request.method == "POST":
            create_tag = CreateTagForm(request.POST)

            if create_tag.is_valid():
                new_tag = create_tag.save(commit=False)
                new_tag.save()
                logger.info(
                    f"Created Tag '{new_tag.value}' from user {request.user.username}"
                )
                messages.success(request, f'Tag "{new_tag.value}" is created!')
                return redirect("blog:create-post")
        else:
            create_tag = CreateTagForm()
    else:
        raise Http404
    return render(request, "blog/tag-creation.html", {"create_tag": create_tag})


def get_ip(request):
    return HttpResponse(request.META["REMOTE_ADDR"])
