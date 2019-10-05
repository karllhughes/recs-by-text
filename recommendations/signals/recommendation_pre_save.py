from django.db.models.signals import pre_save
from django.dispatch import receiver
from recommendations.models import Recommendation
from moviesImporter.models import Movie


@receiver(pre_save, sender=Recommendation)
def recommendation_pre_save(sender, instance, **kwargs):
    movies = Movie.objects.raw('''
        SELECT id, title, year, levenshtein(lower(title), lower(%s)) as difference
        FROM "moviesImporter_movie"
        WHERE levenshtein(lower(title), lower(%s)) < (length(%s) / 4)
        ORDER BY levenshtein(lower(title), lower(%s)) asc, year desc
        LIMIT 5
    ''', [instance.name, instance.name, instance.name, instance.name])
    if movies[0]:
        instance.movie = movies[0]
