from django.contrib import admin
from .models import Category, Article, Commentaire
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["nom", "slug"]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["titre", "auteur", "categorie", "statut", "date_publication"]
    list_filter = ["statut", "categorie"]
    search_fields = ["titre", "contenu"]

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ["auteur", "article", "approuve", "date"]
    list_filter = ["approuve"]
