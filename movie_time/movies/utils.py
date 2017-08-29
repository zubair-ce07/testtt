from dateutil import parser
import tmdbsimple as tmdb
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from movies.models import *


tmdb.API_KEY = '7b43db1b983b055bffd7534a06cafd6c'


def populate_genres():
    response = tmdb.Genres().list()

    for genre in response.get('genres'):
        Genre.objects.get_or_create(name=genre.get('name'), id=genre.get('id'))


def get_person(tmdb_id):
    response = tmdb.People(tmdb_id).info(append_to_response='images')
    birthday = parser.parse(response.get('birthday')) if response.get('birthday') else None
    deathday = parser.parse(response.get('deathday')) if response.get('deathday') else None

    person = Person.objects.create(
        adult=response.get('adult'),
        biography=response.get('biography'),
        birthday=birthday,
        deathday=deathday,
        gender=response.get('gender'),
        homepage=response.get('homepage'),
        tmdb_id=response.get('id'),
        name=response.get('name'),
        place_of_birth=response.get('place_of_birth'),
        popularity=response.get('popularity')
    )

    for image in response.get('images').get('profiles'):
        person.images.create(
            aspect_ratio=image.get('aspect_ratio'),
            file_path=image.get('file_path'),
            height=image.get('height'),
            width=image.get('width'),
            vote_average=image.get('vote_average'),
            vote_count=image.get('vote_count'),
            type=Image.PROFILE
        )

    return person


def get_movie(tmdb_id):
    response = tmdb.Movies(tmdb_id).info(append_to_response='videos,credits')
    print('done', timezone.now())
    release_date = parser.parse(response.get('release_date')) if response.get('release_date') else None

    movie = Movie.objects.create(
        adult=response.get('adult'),
        budget=response.get('budget'),
        homepage=response.get('homepage'),
        tmdb_id=response.get('id'),
        original_language=response.get('original_language'),
        original_title=response.get('original_title'),
        overview=response.get('overview'),
        popularity=response.get('popularity'),
        release_date=release_date,
        revenue=response.get('revenue'),
        runtime=response.get('runtime'),
        status=response.get('status'),
        tag_line=response.get('tagline'),
        title=response.get('title'),
        vote_count=response.get('vote_count'),
        vote_average=response.get('vote_average')
    )

    for genre in response.get('genres'):
        movie.genres.add(Genre.objects.get(id=genre.get('id')))

    for video in response.get('videos').get('results'):
        movie.video_set.create(
            tmdb_id=video.get('id'),
            iso_3166_1=video.get('iso_3166_1'),
            iso_639_1=video.get('iso_639_1'),
            key=video.get('key'),
            name=video.get('name'),
            site=video.get('site'),
            size=video.get('size'),
            type=video.get('type'),
        )

    for role in response.get('credits').get('cast'):
        person = get_or_create_person(role)
        Role.objects.create(
            person=person,
            movie=movie,
            character=role.get('character'),
            credit_id=role.get('credit_id'),
            order=role.get('order'),
        )

    for job in response.get('credits').get('crew'):
        person = get_or_create_person(job)
        Job.objects.create(
            person=person,
            movie=movie,
            department=job.get('department'),
            credit_id=job.get('credit_id'),
            job=job.get('job')
        )

    print(timezone.now())


def get_or_create_person(credit):
    try:
        person = Person.objects.get(tmdb_id=credit.get('id'))
    except ObjectDoesNotExist:
        person = Person.objects.create(
            gender=credit.get('gender'),
            tmdb_id=credit.get('id'),
            name=credit.get('name')
        )
        if credit.get('profile_path'):
            person.images.create(file_path=credit.get('profile_path'),type=Image.PROFILE)
    return person
