from django.db import transaction
from requests.exceptions import HTTPError
import tmdbsimple as tmdb
from movies.models import *


tmdb.API_KEY = '7b43db1b983b055bffd7534a06cafd6c'


def populate_genres():
    response = tmdb.Genres().list()

    for genre in response.get('genres'):
        Genre.objects.get_or_create(name=genre.get('name'), id=genre.get('id'))

    # bug in the TMDB API so before it get fixed this will do
    Genre.objects.get_or_create(id=10769, name='Foreign')


def create_person(tmdb_id):
    response = tmdb.People(tmdb_id).info(append_to_response='images')
    birthday = get_date(response.get('birthday'))
    deathday = get_date(response.get('deathday'))

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
    content_type = ContentType.objects.filter(model='person').first()
    images = create_images(response.get('images').get('profiles'), content_type, person.id, Image.PROFILE)
    Image.objects.bulk_create(images)

    return person


@transaction.atomic
def create_movie(tmdb_id):
    if Movie.objects.filter(tmdb_id=tmdb_id).exists():
        return 'ID: {} - Exists'.format(tmdb_id)
    try:
        response = tmdb.Movies(tmdb_id).info(append_to_response='videos,credits,images')
    except HTTPError as e:
        if e.response.status_code == 404:
            return 'ID: {} - NO ID'.format(tmdb_id)
        else:
            raise
    release_date = get_date(response.get('release_date'))

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

    create_videos(response.get('videos').get('results'), movie)
    create_credits(response.get('credits'), movie)

    content_type = ContentType.objects.filter(model='movie').first()
    backdrops = create_images(response.get('images').get('backdrops'), content_type, movie.id, Image.BACKDROP)
    posters = create_images(response.get('images').get('posters'), content_type, movie.id, Image.POSTER)
    Image.objects.bulk_create(backdrops+posters)

    return 'ID: {} - Success'.format(tmdb_id)


def get_date(date):
    result = None
    if date is not None and date != '':
        year, month, day = parse_date(date)
        result = Date.objects.create(day=day, month=month, year=year)
    return result


def create_credits(credits_data, movie):
    cast = []
    for role in credits_data.get('cast'):
        person = get_or_create_person(role)
        cast.append(Role(
            person=person,
            movie=movie,
            character=role.get('character'),
            credit_id=role.get('credit_id'),
            order=role.get('order'),
        ))
    Role.objects.bulk_create(cast)

    jobs = []
    for job in credits_data.get('crew'):
        person = get_or_create_person(job)
        jobs.append(Job(
            person=person,
            movie=movie,
            department=job.get('department'),
            credit_id=job.get('credit_id'),
            job=job.get('job')
        ))
    Job.objects.bulk_create(jobs)


def create_videos(videos_data, movie):
    videos = []
    for video in videos_data:
        videos.append(Video(
            movie=movie,
            tmdb_id=video.get('id'),
            iso_3166_1=video.get('iso_3166_1'),
            iso_639_1=video.get('iso_639_1'),
            key=video.get('key'),
            name=video.get('name'),
            site=video.get('site'),
            size=video.get('size'),
            type=video.get('type'),
        ))
    Video.objects.bulk_create(videos)


def create_images(images_data, content_type, object_id, img_type):
    images = []
    for image in images_data:
        images.append(Image(
            content_type=content_type,
            object_id=object_id,
            aspect_ratio=image.get('aspect_ratio'),
            file_path=image.get('file_path'),
            height=image.get('height'),
            width=image.get('width'),
            vote_average=image.get('vote_average'),
            vote_count=image.get('vote_count'),
            type=img_type
        ))
    return images


def get_or_create_person(credit):
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
