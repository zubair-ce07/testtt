from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User, Notification, FollowRequest
from movies.serializers import MovieSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    serializes data for user model. Along with user details provides
    with user's own token.
    """
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    relation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'photo', 'email', 'password', 'token', 'relation')

    def get_relation(self, user):
        if self.context.get('request') and not self.context.get('request').user.is_anonymous:
            requesting_user = self.context.get('request').user
            follow_request = FollowRequest.objects.filter(to_user=user, from_user=requesting_user)
            if follow_request.exists():
                return 'followed' if follow_request.first().status == FollowRequest.ACCEPTED else 'request sent'

    def get_token(self, user):
        """
        Checks if requesting user is same as serializing object
        and if are same returns key of token

        Arguments:
            user (User): user being serialized

        Returns:
            token_key (str): key of token associated to user
        """
        if self.context.get('request'):
            return None if user != self.context.get('request').user else user.auth_token.key

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):

    def get_verb(self, notification):
        return notification.get_verb_display()

    def get_action_object(self, notification):
        if notification.verb == Notification.FOLL0W_REQUEST:
            return {'id': notification.object_id, 'status': notification.action_object.get_status_display()}
        elif notification.verb == Notification.MOVIE_RELEASED:
            return MovieSerializer(notification.action_object).data

    def get_actor(self, notification):
        if notification.actor:
            return UserSerializer(notification.actor).data

    verb = serializers.SerializerMethodField()
    action_object = serializers.SerializerMethodField()
    actor = UserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'action_object']
