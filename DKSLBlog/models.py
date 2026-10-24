from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.



class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Catégories"
        ordering = ["nom"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Article(models.Model):
    BROUILLON = "brouillon"
    PUBLIE = "publie"
    STATUT_CHOICES = [
        (BROUILLON, "Brouillon"),
        (PUBLIE, "Publié"),
    ]

    titre = models.CharField(max_length=200)
    # Version du nom pour l'URL
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    # Lien vers l'utilisateur qui a écrit l'article si l'utilisateur est supprimé, ses articles aussi
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    categorie = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
    )
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=BROUILLON)
    date_publication = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_publication"]

    def save(self, *args, **kwargs):
        # Si le slug est vide, on le crée automatiquement à partir du nom
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="commentaires"
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.auteur} sur {self.article}"
