from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from user_management.models import UserProfile, WorkInformation, AcademicInformation, SocialGroup, GroupRequest, \
    FriendRequest

from user_management.serializers import BasicUserSerializer, AcademicInformationPostSerializer, \
    UserDetailSerializer, WorkInformationPostSerializer, UserFriendsSerializer, \
    GroupSerializer, UserSocialGroupsSerializer, NotificationSerializer, GroupRequestSerializer, \
    FriendRequestSerializer


class UsersListCreateView(APIView):
    def get(self, request):
        users = UserProfile.objects.all()
        users_serializer = BasicUserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BasicUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user.auth_user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        user = self.get_object(pk=pk)
        user_serializer = UserDetailSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk=pk)
        user_serializer = UserDetailSerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        user = get_object_or_404(UserProfile, pk=pk)
        if user:
            user.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)


class WorkInformationView(ViewSet):
    def list(self, request):
        username = request.query_params.get('username', None)
        if username:
            work_informations = WorkInformation.objects.filter(user_profile__auth_user__username=username)
        else:
            work_informations = WorkInformation.objects.all()
        work_information_serializer = WorkInformationPostSerializer(work_informations, many=True)
        return Response(work_information_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        work_information_serializer = WorkInformationPostSerializer(data=request.data)
        if work_information_serializer.is_valid():
            work_information_serializer.save()
            return Response(work_information_serializer.data, status=status.HTTP_201_CREATED)
        return Response(work_information_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        work_information = WorkInformation.objects.get(id=pk)
        work_information_serializer = WorkInformationPostSerializer(work_information, data=request.data)
        if work_information_serializer.is_valid():
            work_information_serializer.save()
            return Response(work_information_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        work_information = get_object_or_404(WorkInformation, pk=pk)
        if work_information:
            work_information.delete()
            return Response(work_information, status=status.HTTP_202_ACCEPTED)
        return Response(work_information, status=status.HTTP_404_NOT_FOUND)


class AcademicInformationView(ViewSet):
    def list(self, request):
        username = request.query_params.get('username', None)
        if username:
            academic_informations = AcademicInformation.objects.filter(user_profile__auth_user__username=username)
        else:
            academic_informations = AcademicInformation.objects.all()
        work_informations_serializer = AcademicInformationPostSerializer(academic_informations, many=True)
        return Response(work_informations_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        academic_information_serializer = AcademicInformationPostSerializer(data=request.data)
        if academic_information_serializer.is_valid():
            academic_information_serializer.save()
            return Response(academic_information_serializer.data, status=status.HTTP_201_CREATED)
        return Response(academic_information_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        academic_information = AcademicInformation.objects.get(id=pk)
        academic_information_serializer = AcademicInformationPostSerializer(academic_information, data=request.data)
        if academic_information_serializer.is_valid():
            academic_information_serializer.save()
            return Response(academic_information_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        academic_information = get_object_or_404(AcademicInformation, pk=pk)
        if academic_information:
            academic_information.delete()
            return Response('deleted', status=status.HTTP_202_ACCEPTED)
        return Response('deleted', status=status.HTTP_404_NOT_FOUND)


class GroupsView(ViewSet):
    def list(self, request):
        groups = SocialGroup.objects.all()
        groups_serializer = GroupSerializer(groups, many=True)
        return Response(groups_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(SocialGroup, pk=pk)
        group_serializer = GroupSerializer(group)
        return Response(group_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid():
            group_serializer.save()
            return Response(group_serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        group = SocialGroup.objects.get(id=pk)
        group_serializer = GroupSerializer(group, request.data)
        if group_serializer.is_valid():
            group_serializer.save()
            return Response(group_serializer.validated_data, status=status.HTTP_202_ACCEPTED)
        return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        group = get_object_or_404(SocialGroup, pk=pk)
        if group:
            group.delete()
            return Response(group, status=status.HTTP_202_ACCEPTED)
        return Response(group, status=status.HTTP_202_ACCEPTED)


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
        notification = {
            "text": "You Have a new group join request",
            "status": False,
            "type": "group"
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
            notification = {
                "text": "You Have a new friend request",
                "status": False,
                "type": "friend"
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
        if friend_request:
            friend_request.delete()
            return Response(friend_request, status=status.HTTP_200_OK)
        return Response(friend_request, status=status.HTTP_404_NOT_FOUND)


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
            friend_serializer = BasicUserSerializer(user_from)
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
