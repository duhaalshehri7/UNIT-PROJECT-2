from urllib import request

from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Avg



from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from users.models import DesignerPost,Bookmark,DesignerProfile
from .models import Comment

from django.core.paginator import Paginator



def all_designer_view(request: HttpRequest):
    # posts = DesignerPost.objects.all().order_by("-id")

    posts = DesignerPost.objects.annotate(
        average_rating=Avg("comments__rating")
    ).order_by("-id")

    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)
    posts_page = paginator.get_page(page_number)


    return render(request, 'designer/all_designer_view.html', {'posts': posts_page,})


def post_to_user_view(request: HttpRequest, post_id: int):
    try:
        profile = DesignerPost.objects.get(pk=post_id)
    except DesignerPost.DoesNotExist:
        return redirect("main:main_page_view")

    avg = profile.comments.all().aggregate(Avg("rating"))

    is_bookmarked = Bookmark.objects.filter(
        designer_post=profile,
        user=request.user
    ).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        if request.user.is_authenticated and not request.user.is_designer:
            rating = request.POST.get("rating")
            comment_text = request.POST.get("comment")

            if rating and comment_text:
                Comment.objects.create(
                    designer_post=profile,
                    user=request.user,
                    rating=int(rating),
                    comment=comment_text
                )
                return redirect("designer:post_to_user_view", post_id=post_id)

    comments = profile.comments.all().order_by("-created_at")
    related_designers = DesignerPost.objects.filter(
        designer__specialty=profile.designer.specialty
    ).exclude(id=profile.id)[0:3]

    return render(request, 'designer/view_post_to_user.html', {
        "profile": profile,
        "comments": comments,
        "is_bookmarked": is_bookmarked,
        "related_designer": related_designers,
        "average_rating": avg["rating__avg"]
    })



def search_view(request: HttpRequest):
    search = request.GET.get('search', '').strip()

    availability = request.GET.get('availability')
    specialty = request.GET.get('specialty', '')

    posts = DesignerPost.objects.all()


    if len(search) >= 3:
        posts = DesignerPost.objects.filter(
            Q(designer__user__username__icontains=search) |Q(designer__user__first_name__icontains=search) |
            Q(designer__user__last_name__icontains=search) |Q(designer__specialty__icontains=search)
        ).distinct()

    if availability == 'true':
        posts = posts.filter(availability=True)
    elif availability == 'false':
        posts = posts.filter(availability=False)

    if specialty:
        posts = posts.filter(designer__specialty=specialty)

    return render(request, 'designer/search.html', {'posts': posts,
    'search': search,'availability': availability,'specialty': specialty,'specialty_choices': DesignerProfile.Specialty.choices})