from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from movies.models import Movie
from django.contrib.auth.decorators import login_required

@require_GET
def index(request):
    if request.GET.get('search_keyword'):
        search_keyword = request.GET.get('search_keyword')
        if request.GET.get('search_type') == 'search_by_review_title':
            reviews = Review.objects.filter(title__icontains=search_keyword)
        elif request.GET.get('search_type') == 'search_by_review_content':
            reviews = Review.objects.filter(content__icontains=search_keyword)
        elif request.GET.get('search_type') == 'search_by_review_user':
            reviews = Review.objects.filter(user__username__icontains=search_keyword)
        else:
            if request.GET.get('search_type') == 'search_by_comment_content':
                comments = Comment.objects.filter(content__icontains=search_keyword)
            elif request.GET.get('search_type') == 'search_by_comment_user':
                comments = Comment.objects.filter(user__username__icontains=search_keyword)
            context = {
                'comments': comments,
            }
            return render(request, 'community/index.html', context)
    else:
        reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            movie = get_object_or_404(Movie, pk=movie_pk)
            review.movie_title = movie
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_http_methods(['GET', 'POST'])
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        if review.user == request.user:
            review.delete()
            return redirect('community:index')
        return redirect('community:detail')
    else:
        comments = review.comment_set.all()
        comment_form = CommentForm()
        context = {
            'review': review,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, 'community/detail.html', context)


@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review) 
            if form.is_valid():
                review = form.save()
                return redirect('community:detail', review.pk)          
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('community:detail', review.pk)
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)
    
    
@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete_comment(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('community:detail', review_pk)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        count = review.like_users.count()
        context = {
            'liked': liked,
            'count': count,
        }
        return JsonResponse(context)
    return redirect('accounts:login')
