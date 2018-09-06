from flask import jsonify


def get_favourite_names_by_ids(fav_object, current_user_id, entity_type, entity_value):

    favourites = fav_object.query.filter_by(user_id=current_user_id,
                                                    favourite_entity_id=entity_value).all()
    if favourites:
        favourite_object_ids = [x.favourite_object_id for x in favourites]
        return [entity_type.query.filter_by(_id=the_id).first().name for the_id in favourite_object_ids]
    return 'No favourites'


def get_id_by_name(entity_type, name):
    return entity_type.query.filter_by(name=name).first()._id


def schema_to_json(schema_object, data):
    return jsonify(schema_object.dump(data).data)