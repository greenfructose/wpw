from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Tribe, Membership
from feed.models import Post



def search_tribes(request):
    query = request.GET.get('q')
    object_list = Tribe.objects.filter(name__icontains=query)
    context = {
        'tribes': object_list
    }
    return render(request, "tribes/search_tribes.html", context)


def all_tribes(request):
    tribes = Tribe.objects.all()
    context = {'tribes': tribes}
    return render(request, "tribes/all_tribes.html", context)

@login_required
def tribe_list(request):
    p = request.user.profile
    tribes = p.tribes.all()
    context = {
        'tribes': tribes
    }
    return render(request, "tribes/tribe_list.html", context)

@login_required
def delete_tribe(request, id):
    user_profile = request.user.profile
    tribe = get_object_or_404(Tribe, id=id)
    user_profile.tribes.remove(tribe)
    tribe.members.remove(user_profile)
    return HttpResponseRedirect('/tribes/my-tribes')

@login_required
def tribe_view(request, id):
    tribe = get_object_or_404(Tribe, id=id)
    tribe_posts = Post.objects.filter(tribe=tribe)

    if tribe.members:
        members = tribe.members.all()
    else:
        members = ""
    # Are we in this tribe
    button_status = 'none'
    if tribe not in request.user.profile.tribes.all():
        button_status = 'not_in_tribe'

    context = {
        'posts': tribe_posts,
        'tribe': tribe,
        'button_status': button_status,
        'members': members
        # 'post_count': user_posts.count
    }

    return render(request, "tribes/tribe.html", context)

@login_required
def join_tribe(request, id):
    profile = request.user.profile
    tribe = get_object_or_404(Tribe, id=id)
    profile.tribes.add(tribe)
    tribe.members.add(profile)
    # membership = Membership.objects.create(profile=profile, tribe=tribe)
    return HttpResponseRedirect('/tribes/{}'.format(id))
