from django.contrib import admin

from .models import Categorie, Article, Video, Commentaire_Article,Commentaire_Video, Abonnee, Team

class AbonneAdmin(admin.ModelAdmin):
    list_display = ['email']
    
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['cat_name']
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nomAuteur', 'date')
    
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nomAuteur', 'date')
    
class CommentaireVideoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date')
    
class CommentaireArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date')
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'titre')


# Register your models here.
    
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Commentaire_Article, CommentaireArticleAdmin)
admin.site.register(Commentaire_Video, CommentaireVideoAdmin)
admin.site.register(Abonnee, AbonneAdmin)
admin.site.register(Team, TeamAdmin)