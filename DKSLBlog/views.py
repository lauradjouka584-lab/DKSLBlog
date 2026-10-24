from django.views.generic import ListView, DetailView  
from .models import Article

class ArticleListView(ListView):
    model = Article                          
    template_name = "blog/articles_list.html" 
    context_object_name = "articles"        
    paginate_by = 10                          

    def get_queryset(self):
        return (Article.objects.filter(statut=Article.PUBLIE).select_related("auteur", "categorie"))


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"  
    # On cherche l'article avec son slug dans l'URL 
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Seulement les articles publiés
        return (Article.objects.filter(statut=Article.PUBLIE).select_related("auteur", "categorie"))

    def get_context_data(self, **kwargs):
        # On récupère le contexte normal (contient "article")
        context = super().get_context_data(**kwargs)
        # On ajoute seulement les commentaires approuvés
        context["commentaires"] = (
            self.object.commentaires
            .filter(approuve=True)
            .select_related("auteur")
        )
        return context