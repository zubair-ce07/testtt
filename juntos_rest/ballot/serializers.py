from rest_framework import serializers

from .models import Ballot, Tag, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = ('id', 'text')


class BallotSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Ballot
        fields = ('id', 'title', 'choices', 'tags', 'created_at', 'active_period')

    def create(self, validated_data):

        choices = validated_data.pop('choices')
        tags = validated_data.pop('tags')
        ballot = Ballot.objects.create(**validated_data)

        for tag_name in tags:
            ballot.tags.add(Tag.objects.get(name=tag_name))

        for choice_data in choices:
            Choice.objects.create(ballot=ballot, **choice_data)

        ballot.save()

        return ballot

    def update(self, instance, validated_data):

        choices = validated_data.pop('choices')
        tags = validated_data.pop('tags')

        for choice_data in choices:
            choice = Choice.objects.get(id=choice_data['id'])
            choice.text = choice_data['text']
            choice.save()

        for tag_name in tags:
            tag_present = instance.tags.filter(name=tag_name)
            if not tag_present:
                instance.tags.add(Tag.objects.get(name=tag_name))

        return super().update(instance, validated_data)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(required=True)
