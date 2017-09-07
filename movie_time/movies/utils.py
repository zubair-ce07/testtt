from django.db import transaction
from requests.exceptions import HTTPError
import tmdbsimple as tmdb
from datetime import datetime
from django.conf import settings
from movies.models import *


tmdb.API_KEY = settings.TMDB_API_KEY


def populate_genres():
    response = tmdb.Genres().list()

    for genre in response.get('genres'):
        Genre.objects.get_or_create(name=genre.get('name'), id=genre.get('id'))

    # bug in the TMDB API so before it get fixed this will do
    Genre.objects.get_or_create(id=10769, name='Foreign')


def create_or_update_person(tmdb_id):
    response = tmdb.People(tmdb_id).info(append_to_response='images')
    birthday = get_date(response.get('birthday'))
    deathday = get_date(response.get('deathday'))

    person = Person.objects.update_or_create(
        tmdb_id=response.get('id'),
        defaults={
            'adult': response.get('adult'),
            'biography': response.get('biography'),
            'birthday': birthday,
            'deathday': deathday,
            'gender': response.get('gender'),
            'homepage': response.get('homepage'),
            'name': response.get('name'),
            'place_of_birth': response.get('place_of_birth'),
            'popularity': response.get('popularity')
        },
    )
    content_type = ContentType.objects.filter(model='person').first()
    create_or_update_images(response.get('images').get('profiles'), content_type, person.id, Image.PROFILE)

    return person


@transaction.atomic
def create_or_update_movie(tmdb_id):
    try:
        response = tmdb.Movies(tmdb_id).info(append_to_response='videos,credits,images,recommendations')
    except HTTPError as e:
        if e.response.status_code == 404:
            with open('unavailable_ids.txt', 'a') as unavailable_ids_file:
                unavailable_ids_file.write('{tmdb_id}\n'.format(tmdb_id=tmdb_id))
            return 'ID: {} - NO ID'.format(tmdb_id)
        else:
            raise
    release_date = get_date(response.get('release_date'))
    then = datetime.now()
    movie, created = Movie.objects.update_or_create(
        tmdb_id=response.get('id'),
        defaults={
            'adult': response.get('adult'),
            'budget': response.get('budget'),
            'homepage': response.get('homepage'),
            'original_language': response.get('original_language'),
            'original_title': response.get('original_title'),
            'overview': response.get('overview'),
            'popularity': response.get('popularity'),
            'release_date': release_date,
            'revenue': response.get('revenue'),
            'runtime': response.get('runtime'),
            'status': response.get('status'),
            'tag_line': response.get('tagline'),
            'title': response.get('title'),
            'vote_count': response.get('vote_count'),
            'vote_average': response.get('vote_average')
        }
    )

    added_genres = movie.genres.all()
    for item in response.get('genres'):
        genre = Genre.objects.get(id=item.get('id'))
        if genre not in added_genres:
            movie.genres.add(genre)

    added_recommendations = movie.recommendations.all()
    for item in response.get('recommendations').get('results'):
        recommendation, created = Movie.objects.get_or_create(tmdb_id=item.get('id'))
        if recommendation not in added_recommendations:
            movie.recommendations.add(recommendation)

    create_or_update_videos(response.get('videos').get('results'), movie)
    create_or_update_credits(response.get('credits'), movie)

    content_type = ContentType.objects.filter(model='movie').first()
    create_or_update_images(response.get('images').get('backdrops'), content_type, movie.id, Image.BACKDROP)
    create_or_update_images(response.get('images').get('posters'), content_type, movie.id, Image.POSTER)
    return 'ID: {} - Success - {}'.format(tmdb_id, datetime.now() - then)


def get_date(date):
    result = None
    if date is not None and date != '':
        year, month, day = parse_date(date)
        result = Date.objects.create(day=day, month=month, year=year)
    return result


def create_or_update_credits(credits_data, movie):
    for role in credits_data.get('cast'):
        person = get_or_create_person(role)
        Role.objects.update_or_create(
            credit_id=role.get('credit_id'),
            defaults={
                'person': person,
                'movie': movie,
                'character': role.get('character'),
                'order': role.get('order')
            }
        )

    for job in credits_data.get('crew'):
        person = get_or_create_person(job)
        Job.objects.update_or_create(
            credit_id=job.get('credit_id'),
            defaults={
                'person': person,
                'movie': movie,
                'department': job.get('department'),
                'job': job.get('job')
            }
        )


def create_or_update_videos(videos_data, movie):
    for video in videos_data:
        if video.get('key') is not None:
            Video.objects.update_or_create(
                tmdb_id=video.get('id'),
                defaults={
                    'iso_3166_1': video.get('iso_3166_1'),
                    'iso_639_1': video.get('iso_639_1'),
                    'key': video.get('key'),
                    'name': video.get('name'),
                    'site': video.get('site'),
                    'size': video.get('size'),
                    'type': video.get('type'),
                    'movie': movie
                },
            )


def create_or_update_images(images_data, content_type, object_id, img_type):
    for image in images_data:
        Image.objects.update_or_create(
            file_path=image.get('file_path'),
            defaults={
                'content_type': content_type,
                'object_id': object_id,
                'aspect_ratio': image.get('aspect_ratio'),
                'height': image.get('height'),
                'width': image.get('width'),
                'vote_average': image.get('vote_average'),
                'vote_count': image.get('vote_count'),
                'type': img_type
            },
        )


def get_or_create_person(credit):
    profile_image = Image.objects.filter(file_path=credit.get('profile_path'))
    if profile_image.exists():
        person = Person.objects.get(id=profile_image.first().object_id)
    else:
        person, created = Person.objects.get_or_create(
            tmdb_id=credit.get('id'),
            defaults={
                'gender': credit.get('gender'),
                'name': credit.get('name')
            }
        )
        if credit.get('profile_path') and created:
            person.images.create(file_path=credit.get('profile_path'), type=Image.PROFILE)
    return person


def parse_date(date):
    bits = date.split('-')

    if len(date) == 4:
        result = (bits[0], 0, 0)
    elif len(date) == 7:
        result = (bits[0], bits[1], 0)
    elif len(date) == 10:
        result = (bits[0], bits[1], bits[2])
    else:
        result = None

    return result


def get_changed_movies_ids(start_date, end_date):
    changes = tmdb.Changes().movie(start_date=start_date, end_date=end_date)
    changed_movies_ids = changes.get('results')
    for page in range(2, changes.get('total_pages') + 1):
        changes = tmdb.Changes().movie(page=page, start_date=start_date, end_date=end_date)
        changed_movies_ids += changes.get('results')
    return changed_movies_ids
