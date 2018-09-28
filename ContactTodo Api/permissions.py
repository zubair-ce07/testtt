from rest_framework.permissions import BasePermission, SAFE_METHODS


class can_add_contact(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.user == request.user


class can_add_item(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        todos = user.Todos.all()
        flag = obj.todo in todos
        return flag

    def has_permission(self, request, view):
        obj = request.data.get('todo')
        if obj:
            user = request.user
            todos = [t.id for t in user.Todos.all()]
            flag = int(obj) in todos
        else:
            flag = True
        return flag


class is_logged_in(BasePermission):
    def has_permission(self, request, view):
        return request.user
