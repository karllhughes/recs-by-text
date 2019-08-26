import csv
import sys
from moviesImporter.models import Movie
from IPython import embed

def run():
    csv.field_size_limit(sys.maxsize)
    with open('moviesImporter/data_to_import/title.basics.tsv') as tsvfile:
        basics = csv.DictReader(tsvfile, dialect='excel-tab')
        with open('moviesImporter/data_to_import/title.crew.tsv') as tsvfile:
            crew_members = list(csv.DictReader(tsvfile, dialect='excel-tab'))
            
            for title in basics:
                if title['titleType'] == 'movie' and title['genres'] and title['startYear']:
                    found_index = None
                    for index, crew in enumerate(crew_members):
                        if crew['tconst'] == title['tconst'] and crew['directors'] != '\\N':
                            try: 
                                found_index = index
                                movie_dict = create_movie_dict(crew, title)
                                Movie(**movie_dict).save()
                                break 
                            except Exception as e:
                                print(e)
                                print(f"{title['primaryTitle']} did not save.") 

                    if found_index:
                        del crew_members[found_index]


def create_movie_dict(crew, title):
    directors = crew['directors'].split(',')
    genres = title['genres'].split(',')
    genre_length = len(genres)
    directors_length = len(directors)
    movie = {
        'imdb_id' : title['tconst'],
        'title': title['primaryTitle'],
        'year': title['startYear'],
        'director_1': directors[0] if directors_length > 0 else None,
        'director_2': directors[1] if directors_length > 1 else None,
        'director_3': directors[2] if directors_length > 2 else None,
        'genre_1' : genres[0] if genre_length > 0 else None, 
        'genre_2' : genres[1] if genre_length > 1  else None, 
        'genre_3' : genres[2] if genre_length > 2  else None, 
    }
    # embed()
    return movie



# if is movie and has genre and has release year
# search crew and get match and save director ids, split on comma. 