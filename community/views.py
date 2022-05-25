from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from movies.models import Movie
from django.contrib.auth.decorators import login_required
import math

@require_GET
def index(request):
    search_keyword = request.GET.get('search_keyword')
    search_type = request.GET.get('search_type')
    typeof = request.GET.get('typeof')
    if typeof == 'None' or not typeof:
        typeof = 'created_at_des'
    page = request.GET.get('page')
    if page=='None' or not page:
        page = 1
    else:
        page = int(page)
    reviews_or_comments = request.GET.get('reviews_or_comments')
    if reviews_or_comments == 'None' or not reviews_or_comments:
        reviews_or_comments = 'reviews'
    if reviews_or_comments == 'reviews':
        reviews = Review.objects.all()
        if search_keyword == 'None' or not search_keyword:
            pass
        else:
            if search_type == 'search_by_review_title':
                reviews = reviews.filter(title__icontains=search_keyword)
            elif search_type == 'search_by_review_content':
                reviews = reviews.filter(content__icontains=search_keyword)
            elif search_type == 'search_by_review_user':
                reviews = reviews.filter(user__username__icontains=search_keyword)
            elif search_type == 'search_by_movie_title':
                reviews = reviews.filter(movie_title__title__icontains=search_keyword)
        if typeof == 'created_at_asc':
            reviews = reviews.order_by('created_at')
        elif typeof == 'created_at_des':
            reviews = reviews.order_by('-created_at')
        elif typeof == 'rank_asc':
            reviews = reviews.order_by('rank')
        elif typeof == 'rank_des':
            reviews = reviews.order_by('-rank')
        elif typeof == 'like_users_asc':
            reviews = reviews.order_by('-like_users')
        elif typeof == 'like_users_des':
            reviews = reviews.order_by('-like_users')
        valid_page = math.ceil(len(reviews) / 15)
        reviews = reviews[15 * (page - 1):15 * page]
    elif reviews_or_comments == 'comments':
        comments = Comment.objects.all()
        if search_keyword == 'None' or not search_keyword:
            pass
        else:
            if request.GET.get('search_type') == 'search_by_comment_content':
                comments = comments.filter(content__icontains=search_keyword)
            elif request.GET.get('search_type') == 'search_by_comment_user':
                comments = comments.filter(user__username__icontains=search_keyword)
        if typeof == 'created_at_asc':
            comments = comments.order_by('created_at')
        elif typeof == 'created_at_des':
            comments = comments.order_by('-created_at')
        valid_page = math.ceil(len(comments) / 15)
        comments = comments[15 * (page - 1):15 * page]
    pagelist = request.GET.get('pagelist')
    if pagelist == 'None' or not pagelist:
        pagelist = 1
    else:
        pagelist = int(pagelist)
    pagenumbers = [i for i in range(10 * pagelist - 9, 10 * pagelist + 1)]
    valid_pages = [i for i in range(1, valid_page + 1)]
    valid_pagelist = math.ceil(valid_page / 10)
    valid_pagelists = [i for i in range(1, valid_pagelist)]
    if reviews_or_comments == 'reviews':
        print(reviews)
        context = {
            'reviews': reviews,
            'typeof': typeof,
            'pagelist': pagelist,
            'pagenumbers': pagenumbers,
            'page': page,
            'search_keyword': search_keyword,
            'search_type': search_type,
            'valid_pages': valid_pages,
            'valid_pagelists' : valid_pagelists,
            'reviews_or_comments' : reviews_or_comments,
        }
    elif reviews_or_comments == 'comments':
        context = {
            'comments': comments,
            'typeof': typeof,
            'pagelist': pagelist,
            'pagenumbers': pagenumbers,
            'page': page,
            'search_keyword': search_keyword,
            'search_type': search_type,
            'valid_pages': valid_pages,
            'valid_pagelists' : valid_pagelists,
            'reviews_or_comments' : reviews_or_comments,
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
