from rest_framework.serializers import ModelSerializer, SerializerMethodField

from web.issue.models import Issue, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model= Comment
        fields = [
            'id',
            'issue_id',
            'comment_by',
            'comment',
            'timestamp',
            'last_edit'
        ]


class IssueCreateUpdateSerializer(ModelSerializer):
    comments = SerializerMethodField()
    created_by = SerializerMethodField()
    manage_by = SerializerMethodField()
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'image',
            'created_by',
            'manage_by',
            'comments'
        ]

    def get_comments(self, obj):
        issue_comments = Comment.objects.filter(issue_id=obj.id)
        return CommentSerializer(issue_comments, many=True).data

    def get_created_by(self, obj):
        return str(obj.created_by.username)

    def get_manage_by(self, obj):
        if obj.manage_by:
            return str(obj.manage_by.username)
        return None

class IssueStatusChangeSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'status'
        ]
