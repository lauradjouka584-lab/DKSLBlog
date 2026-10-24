from django.urls import path
from DKSLBlog.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('liste_articles/', ArticleListView, name='liste_articles'),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="detail"),

]