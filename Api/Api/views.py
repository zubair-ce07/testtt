from flask import abort
from flask import jsonify
from flask import request

from Api import app
from .models import TodoList, TodoListSchema, db

todo_item_schema = TodoListSchema()
todo_list_schema = TodoListSchema(many=True)


@app.route("/todo/api", methods=["POST"])
def add_item():
    """endpoint to create new todo_item"""
    if 'title' in request.json and 'description' in request.json:
        title = request.json['title']
        description = request.json['description']
        todo_item = TodoList(title, description)
        db.session.add(todo_item)
        db.session.commit()
        return todo_item_schema.jsonify(todo_item)
    abort(400)


@app.route("/todo/api", methods=["GET"])
def get_todo_list():
    """endpoint to show all todo items"""
    todo_list = TodoList.query.all()
    result = todo_list_schema.dump(todo_list)
    return jsonify(result.data)


@app.route("/todo/api/<id>", methods=["GET"])
def get_todo_item(id):
    """endpoint to get todo_item detail by id"""
    todo_item = TodoList.query.get(id)
    if todo_item:
        return todo_item_schema.jsonify(todo_item)
    return abort(404)


@app.route("/todo/api/<id>", methods=["PUT"])
def item_update(id):
    """endpoint to update todo item"""
    todo_item = TodoList.query.get(id)
    if todo_item:
        title = request.json.get('title', todo_item.title)
        description = request.json.get('description', todo_item.desc)
        todo_item.title = title
        todo_item.description = description
        db.session.commit()
        return todo_item_schema.jsonify(todo_item)
    else:
        return abort(404)


@app.route("/todo/api/<id>", methods=["DELETE"])
def item_delete(id):
    """endpoint to delete todo_item"""
    todo_item = TodoList.query.get(id)
    if todo_item:
        db.session.delete(todo_item)
        db.session.commit()
        return todo_item_schema.jsonify(todo_item)
    return abort(404)
