from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .forms import CommentFormArticle, CommentFormVideo, AbonneeForm
from .models import Article, Abonnee, Categorie, Commentaire_Article, Commentaire_Video, Video, Team
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import uuid
from django.core.mail import send_mail
from django.conf import settings
import re


def acceuil(request):
    my_articles = Article.objects.all()[:2]
    my_videos = Video.objects.all()[:4]
    
    
    if request.method == 'POST':
        form = AbonneeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                abonnee = Abonnee.objects.get(email=email)
                response = {'status': 'exists', 'message': 'Cet email est déjà souscrit.'}
            except Abonnee.DoesNotExist:
                abonnee = Abonnee.objects.create(email=email)
                response = {'status': 'success', 'message': 'Votre courriel a été inscrit avec succès.'}
            return JsonResponse(response)
    else:
        form = AbonneeForm()
        
    context = {
        'myArticles': my_articles,
        'myVideos': my_videos,
        'form': form,
    }
    return render(request, 'acceuil.html', context)



def recevoirJesus(request):
    return render(request, 'recevoirJesus.html')


def notreEquipe(request):
    team = Team.objects.all()
    
    context = {
        'team':team,
    }
    return render(request, 'notreEquipe.html', context)


def contact(request):
    return render(request, 'contact.html')


def video(request):
    videos_per_page = 6
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    categorie = Categorie.objects.all()
    
    selected_categorie = request.GET.get('categorie', '')
    videos = Video.objects.all().order_by('date')
    
    if search_query:
        videos = videos.filter(titre__icontains=search_query)
    if selected_categorie:
        videos = videos.filter(f_categorie_id=selected_categorie)
    
    paginator = Paginator(videos, videos_per_page)
    page = paginator.get_page(page_number)
    
    context = {
        'page': page,
        'search_query': search_query,
        'categorie':categorie,
        'selected_categorie':selected_categorie
    }
    
    return render(request, 'video.html', context)



def text(request):
    articles_per_page = 6
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    
    articles = Article.objects.all().order_by('date')
    selected_categorie = request.GET.get('categorie', '')
    categorie = Categorie.objects.all()
    
    
    if search_query:
        articles = articles.filter(titre__icontains=search_query)
    if selected_categorie:
        articles = articles.filter(f_categorie_id=selected_categorie)

    paginator = Paginator(articles, articles_per_page)
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'search_query': search_query,
        'categorie':categorie,
        'selected_categorie':selected_categorie
    }
    return render(request, 'text.html', context)


def handle_comment(request, form, instance):
    if form.is_valid():
        comment = form.save(commit=False)
        if isinstance(instance, Article):
            comment.f_article = instance
        elif isinstance(instance, Video):
            comment.f_video = instance
        comment.save()

        return JsonResponse({
            'success': True,
            'comment': {
                'author': comment.nom,
                'created_at': comment.date,
                'text': comment.commentaire
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })



def player_text(request, slug):
    article_detail = get_object_or_404(Article, slug=slug)
    comments = Commentaire_Article.objects.filter(f_article=article_detail)
    categorie = article_detail.f_categorie
    total_comments = comments.count()

    if request.method == 'POST':
        form = CommentFormArticle(request.POST)
        return handle_comment(request, form, article_detail)
    else:
        form = CommentFormArticle()

    context = {
        'Detail': article_detail,
        'comments': comments,
        'total_comments': total_comments,
        'form': form,
        'categorie':categorie
    }
    return render(request, 'player_text.html', context)


@never_cache
def player_video(request, slug):
    video_detail = get_object_or_404(Video, slug=slug)
    comments = Commentaire_Video.objects.filter(f_video=video_detail)
    categorie = video_detail.f_categorie
    total_comments = comments.count()
    if request.method == 'POST':
        form = CommentFormVideo(request.POST)
        return handle_comment(request, form, video_detail)
    else:
        form = CommentFormVideo()

    context = {
        'Detail': video_detail,
        'comments': comments,
        'total_comments': total_comments,
        'form': form,
        'categorie':categorie
    }

    return render(request, 'player_video.html', context)













# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse
# from .forms import CommentFormArticle, CommentFormVideo
# from .models import Article, Abonnee, Categorie, Commentaire_Article,Commentaire_Video, Video
# from django.http import JsonResponse
# from django.views.decorators.cache import never_cache
# from django.core.paginator import Paginator
# import uuid


# def acceuil(request):
#     myArticles = Article.objects.all()[:2]
#     myVideos = Video.objects.all()[:4]
#     context = {
#         'myArticles': myArticles,
#         'myVideos':myVideos
#         }
#     return render(request, 'acceuil.html', context)

# def categorie(request):
#     return render(request, 'categorie.html')

# def apropos(request):
#     return render(request, 'apropos.html')

# def contact(request):
#     return render(request, 'contact.html')



# def video(request):
#     videos_per_page = 6
#     page_number = request.GET.get('page', 1)  # Get the current page number from the query parameters
#     videos = Video.objects.all()
    
#     paginator = Paginator(videos, videos_per_page)
#     page = paginator.get_page(page_number)
    
#     context = {
#         'page': page,
#     }
#     return render(request, 'video.html', context)



# def text(request):
#     articles_per_page = 6
#     page_number = request.GET.get('page', 1)  # Get the current page number from the query parameters
#     articles = Article.objects.all()

#     paginator = Paginator(articles, articles_per_page)
#     page = paginator.get_page(page_number)

#     context = {
#         'page': page,
#     }
#     return render(request, 'text.html', context)

# def get_machine_identifier(request):
#     ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR', '')
#     return ip_address



# def player_text(request, pk):
#     articleDetail = get_object_or_404(Article, pk=pk)
#     comments = Commentaire_Article.objects.filter(f_article=articleDetail)
#     total_comments = comments.count()

#     if request.method == 'POST':
#         form = CommentFormArticle(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.f_article = articleDetail
#             comment.save()
            
#             return JsonResponse({'success': True, 'comment': {'author': comment.nom, 'created_at': comment.date, 'text': comment.commentaire}})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = CommentFormArticle()

#     context = {
#         'Detail': articleDetail,
#         'comments': comments,
#         'total_comments': total_comments,
#         'form': form,
#     }
#     return render(request, 'player_text.html', context)



# @never_cache
# def player_video(request, pk):
#     videoDetail = get_object_or_404(Video, pk=pk)
#     comments = Commentaire_Video.objects.filter(f_video=videoDetail)
#     total_comments = comments.count()

#     if request.method == 'POST':
#         form = CommentFormVideo(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.f_video = videoDetail
#             comment.save()
            
#             return JsonResponse({'success': True, 'comment': {'author': comment.nom, 'created_at': comment.date, 'text': comment.commentaire}})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         form = CommentFormVideo()

#     context = {
#         'Detail': videoDetail,
#         'comments': comments,
#         'total_comments': total_comments,
#         'form': form,
#     }

#     return render(request, 'player_video.html', context)
