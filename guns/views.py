from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import Gun
from django.http import JsonResponse



@require_GET
def index(request):
    if request.GET.get('search_keyword'):
        search_keyword = request.GET.get('search_keyword')
        if request.GET.get('search_type') == 'search_by_name':
            guns = Gun.objects.filter(gun_name__icontains=search_keyword)
        elif request.GET.get('search_type') == 'search_by_type':
            guns = Gun.objects.filter(gun_type__type_name__icontains=search_keyword)
    else:
        guns = Gun.objects.all()
    context = {
        'guns': guns,
    }
    return render(request, 'guns/index.html', context)


@require_GET
def detail(request, gun_pk):
    gun = get_object_or_404(Gun, pk=gun_pk)
    context = {
        'gun': gun,
    }
    return render(request, 'guns/detail.html', context)


@require_POST
def like(request, gun_pk):
    if request.user.is_authenticated:
        gun = get_object_or_404(Gun, pk=gun_pk)
        user = request.user

        if gun.like_users.filter(pk=user.pk).exists():
            gun.like_users.remove(user)
            liked = False
        else:
            gun.like_users.add(user)
            liked = True
        count = gun.like_users.count()
        context = {
            'liked': liked,
            'count': count,
        }
        return JsonResponse(context)
    return redirect('accounts:login')