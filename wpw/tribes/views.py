from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Tribe, Membership
from users.models import Profile


@login_required
def search_tribes(request):
    query = request.GET.get('q')
    object_list = Tribe.objects.filter(name__icontains=query)
    context = {
        'tribes': object_list
    }
    return render(request, "tribes/search_tribes.html", context)


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
    return HttpResponseRedirect('/users/{}'.format(user_profile.slug))

@login_required
def tribe_view(request, slug):
    tribe = Tribe.objects.filter(slug=slug).first()
    # user_posts = Post.objects.filter(user_name=u)

    members = tribe.members.all()

    # Are we in this tribe
    button_status = 'none'
    if tribe not in request.user.profile.tribes.all():
        button_status = 'not_in_tribe'

    context = {
        'tribe': tribe,
        'button_status': button_status,
        'members': members
        # 'post_count': user_posts.count
    }

    return render(request, "tribes/tribe.html", context)

@login_required
def join_tribe(request, id):
    profile = request.user.profile
    tribe = Tribe.objects.filter(id=id)
    membership = Membership.objects.get_or_create(profile=profile, tribe=tribe)
    return HttpResponseRedirect('/tribes/{}'.format(tribe.slug))
