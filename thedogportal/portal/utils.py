from random import randint

from .models import Profile, Uploads, Upvotes, Downvotes, Favorites


def get_single_upload_by_id(id):
    return Uploads.objects.filter(image_identifier=id)[0]


def get_user_by_id(id):
    return Profile.objects.get(pk=id)


def get_upvotes_object(upvoter, photo, owner):
    return Upvotes.objects.filter(upvoter=upvoter,
                                  photo=photo,
                                  owner=owner)


def get_downvotes_object(downvoter, photo, owner):
    return Downvotes.objects.filter(downvoter=downvoter,
                                    photo=photo,
                                    owner=owner)


def get_favorites_object(favoriter, photo, owner):
    return Favorites.objects.filter(favoriter=favoriter,
                                    photo=photo,
                                    owner=owner)


def get_id_excluded_upload_count(id):
    return Uploads.objects.exclude(owner=id).count()


def get_id_excluded_random_upload(id, count):
    return Uploads.objects.exclude(owner=id)[randint(0, count - 1)]


def delete_single_upload_by_id(id):
    return Uploads.objects.filter(image_identifier=id)[0].delete()


def delete_upvotes_object(upvoter, photo, owner):
    return get_upvotes_object(upvoter=upvoter,
                              photo=photo,
                              owner=owner).delete()


def delete_downvotes_object(downvoter, photo, owner):
    return get_downvotes_object(downvoter=downvoter,
                                photo=photo,
                                owner=owner).delete()


def delete_favorites_object(favoriter, photo, owner):
    return get_favorites_object(favoriter=favoriter,
                                photo=photo,
                                owner=owner).delete()


def new_upvotes_instance(upvoter, photo, owner):
    return Upvotes(upvoter=upvoter,
                   photo=photo,
                   owner=owner)


def new_downvotes_instance(downvoter, photo, owner):
    return Downvotes(downvoter=downvoter,
                     photo=photo,
                     owner=owner)


def new_favorites_instance(favoriter, photo, owner):
    return Favorites(favoriter=favoriter,
                     photo=photo,
                     owner=owner)
