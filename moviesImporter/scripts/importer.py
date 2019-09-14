import csv
import sys
from moviesImporter.models import Movie
from datetime import datetime


def run():
    startTime = datetime.now()
    csv.field_size_limit(sys.maxsize)
    with open('moviesImporter/data_to_import/title.basics.tsv', 'r') as basics_file:
        basics = csv.DictReader(basics_file, dialect='excel-tab')
        with open('moviesImporter/data_to_import/title.crew.tsv', 'r') as crew_file:
            movies_to_save = []
            crew_file_array = list(csv.reader(crew_file, dialect='excel-tab'))
            c = 0
            for index, title in enumerate(basics):
                if title['titleType'] == 'movie' and title['genres'] and title['genres'] != '\\N' and title['startYear'] and title['startYear'] != '\\N':
                    crew_line = crew_file_array[index + 1]
                    if crew_line and crew_line[0] == title['tconst'] and crew_line[1] != '\\N':
                        try:
                            movie_dict = create_movie_dict(crew_line, title)
                            c += 1
                            movies_to_save.append(Movie(**movie_dict))
                        except Exception as e:
                            print(e)
                            print(f"{title['primaryTitle']} did not save.")

            Movie.objects.bulk_create(movies_to_save)
            print(str(c) + ' great movies imported!')
            print(datetime.now() - startTime)


def create_movie_dict(crew, title):
    directors = crew[1].split(',')
    genres = title['genres'].split(',')
    genre_length = len(genres)
    directors_length = len(directors)
    movie = {
        'imdb_id': title['tconst'],
        'title': title['primaryTitle'],
        'year': title['startYear'],
        'director_1': directors[0] if directors_length > 0 else None,
        'director_2': directors[1] if directors_length > 1 else None,
        'director_3': directors[2] if directors_length > 2 else None,
        'genre_1': genres[0] if genre_length > 0 else None,
        'genre_2': genres[1] if genre_length > 1 else None,
        'genre_3': genres[2] if genre_length > 2 else None,
    }
    return movie
