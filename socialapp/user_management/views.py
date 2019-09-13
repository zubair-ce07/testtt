from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet, ModelViewSet

from user_management.models import UserProfile, WorkInformation, AcademicInformation, SocialGroup, GroupRequest, \
    FriendRequest

from user_management.serializers import (
    UserProfileSerializer, AcademicInformationPostSerializer, \
    UserDetailSerializer, WorkInformationPostSerializer, UserFriendsSerializer, \
    GroupSerializer, UserSocialGroupsSerializer, NotificationSerializer, GroupRequestSerializer, \
    FriendRequestSerializer, WorkInformationGetSerializer, AcademicInformationGetSerializer
)

from user_management.utils import get_notification_text

from user_management.utils import NOTIFICATION_CHOICE_FIELDS


class UsersListCreateView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer


class WorkInformationView(ModelViewSet):
    queryset = WorkInformation.objects.all()
    serializer_class = WorkInformationPostSerializer

    def list(self, request, *args, **kwargs):
        username = request.query_params.get('username', None)
        if username:
            work_informations = WorkInformation.objects.filter(user_profile__username=username)
        else:
            work_informations = WorkInformation.objects.all()

        work_information_serializer = WorkInformationGetSerializer(work_informations, many=True)
        return Response(work_information_serializer.data, status=status.HTTP_200_OK)


class AcademicInformationView(ModelViewSet):
    queryset = AcademicInformation.objects.all()
    serializer_class = AcademicInformationPostSerializer

    def list(self, request, *args, **kwargs):
        username = request.query_params.get('username', None)
        if username:
            academic_informations = AcademicInformation.objects.filter(user_profile__username=username)
        else:
            academic_informations = AcademicInformation.objects.all()
        work_informations_serializer = AcademicInformationGetSerializer(academic_informations, many=True)
        return Response(work_informations_serializer.data, status=status.HTTP_200_OK)


class GroupRequestView(ViewSet):
    def list(self, request, **kwargs):
        group_requests = GroupRequest.objects.filter(status=False, user__id=kwargs['pk'])
        group_requests_serializer = GroupRequestSerializer(group_requests, many=True)
        return Response(group_requests_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        pk_user = kwargs['user_id']
        pk_group = kwargs['group_id']
        group_request = {
            'user': pk_user,
            'group': pk_group,
            'status': False
        }
        notification_type = NOTIFICATION_CHOICE_FIELDS.__dict__['group']
        notification = {
            "text": get_notification_text(notification_type),
            "status": False,
            "type": notification_type
        }
        group_request_serializer = GroupRequestSerializer(data=group_request)
        notification_serializer = NotificationSerializer(data=notification)

        if group_request_serializer.is_valid():
            if notification_serializer.is_valid():
                group_request_serializer.save()
                notification_serializer.save()
                urls = {
                    'url_accept': reverse(viewname='add-group', args=[pk_user, pk_group]),
                    'url_accept_method': 'post',
                    'url_reject': reverse(viewname='cancel-group-request', args=[pk_user, pk_group]),
                    'url_reject_method': 'delete'
                }

                return Response(urls, status=status.HTTP_200_OK)
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(group_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        group_request = get_object_or_404(GroupRequest, **kwargs)
        if group_request:
            group_request.delete()
            return Response(group_request, status=status.HTTP_200_OK)
        return Response(group_request, status=status.HTTP_200_OK)


class GroupsView(ModelViewSet):
    queryset = SocialGroup.objects.all()
    serializer_class = GroupSerializer


class FriendRequestView(ViewSet):
    def list(self, request, **kwargs):
        friend_requests = FriendRequest.objects.filter(status=False, request_to__id=kwargs['pk'])
        friend_requests_serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(friend_requests_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        pk_user_to = kwargs['request_to_id']
        pk_user_from = kwargs['request_from_id']
        if pk_user_from == pk_user_to:
            return Response('The person who sent the request and who received cant be same')
        else:
            friend_request = {
                'request_to': pk_user_to,
                'request_from': pk_user_from,
                'status': False
            }
            notification_type = NOTIFICATION_CHOICE_FIELDS.__dict__['friend']
            notification = {
                "text": get_notification_text(notification_type),
                "status": False,
                "type": notification_type
            }
            friend_request_serializer = FriendRequestSerializer(data=friend_request)
            notification_serializer = NotificationSerializer(data=notification)

            if friend_request_serializer.is_valid():
                if notification_serializer.is_valid():
                    friend_request_serializer.save()
                    notification_serializer.save()
                    urls = {
                        'url_accept': reverse(viewname='add-friend', args=[pk_user_to, pk_user_from]),
                        'url_accept_method': 'post',
                        'url_reject': reverse(viewname='cancel-friend-request', args=[pk_user_to, pk_user_from]),
                        'url_reject_method': 'delete'
                    }

                    return Response(urls, status=status.HTTP_200_OK)
                return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(friend_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        friend_request = get_object_or_404(GroupRequest, **kwargs)
        friend_request.delete()
        return Response(friend_request, status=status.HTTP_200_OK)


class JoinGroupsView(ViewSet):
    def list(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        if user:
            groups_serializer = UserSocialGroupsSerializer(user.social_groups, many=True)
            return Response(groups_serializer.data, status=status.HTTP_200_OK)
        return Response(user, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        group = get_object_or_404(SocialGroup, pk=kwargs['pk_group'])
        if user and group:
            joined_group = get_object_or_404(user.social_groups, pk=group.id)
            group_serializer = GroupSerializer(joined_group)
            return Response(group_serializer.data, status=status.HTTP_200_OK)
        if not user:
            return Response(user, status=status.HTTP_404_NOT_FOUND)
        return Response(group, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        group = get_object_or_404(SocialGroup, pk=kwargs['pk_group'])
        if user and group:
            user.social_groups.add(group)

            group_request = GroupRequest.objects.get(group__id=group.id, request_to__id=user.id)
            group_request.status = True
            group_request.save()

            return Response('member added', status=status.HTTP_200_OK)
        if not user:
            return Response(user, status=status.HTTP_404_NOT_FOUND)
        return Response(group, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        group = get_object_or_404(SocialGroup, pk=kwargs['pk_group'])
        if user and group:
            user.social_groups.remove(group)
            return Response('member removed', status=status.HTTP_200_OK)
        if not user:
            return Response(user, status=status.HTTP_404_NOT_FOUND)
        return Response(group, status=status.HTTP_404_NOT_FOUND)


class FriendsView(ViewSet):
    def list(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        if user:
            friends_serializer = UserFriendsSerializer(user)
            return Response(friends_serializer.data, status=status.HTTP_200_OK)
        return Response(user, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, **kwargs):
        user_from = UserProfile.objects.filter(friends__user_from__id=kwargs['pk_friend'])
        if user_from:
            friend_serializer = UserProfileSerializer(user_from)
            return Response(friend_serializer.data, status=status.HTTP_200_OK)
        return Response(user_from, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        friend = get_object_or_404(UserProfile, pk=kwargs['pk_friend'])
        if user and friend:
            user.friends.add(friend)
            friend.friends.add(user)

            friend_request = FriendRequest.objects.get(request_from__id=friend.id, request_to__id=user.id)
            friend_request.status = True
            friend_request.save()

            return Response('friend added', status=status.HTTP_200_OK)
        if not user:
            return Response(user, status=status.HTTP_404_NOT_FOUND)
        return Response(friend, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, **kwargs):
        user = get_object_or_404(UserProfile, pk=kwargs['pk_user'])
        friend = get_object_or_404(UserProfile, pk=kwargs['pk_friend'])
        if user and friend:
            user.friends.remove(friend)
            friend.friends.remove(user)
            return Response(friend, status=status.HTTP_200_OK)
        if not user:
            return Response(user, status=status.HTTP_404_NOT_FOUND)
        return Response(friend, status=status.HTTP_404_NOT_FOUND)
