from rest_framework import serializers

from events.models import Event, Rsvp


class EventSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField('owner_display')
    #has_confirmed = serializers.SerializerMethodField('rsvp')

    class Meta:
        model = Event
        fields = ('pk', 'title', 'date', 'description', 'participants', 'owner_id', 'owner_username')
        read_only_fields = ('participants',)
        lookup_field = 'pk'

    def owner_display(self, event):
        return event.owner.username

    def create(self, validated_data):
        event = Event(**validated_data)
        event.owner = self.context['request'].user
        event.save()
        return event


class RsvpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rsvp
        fields = ('event', 'user')

    def create(self, validated_data):
        rsvp = Rsvp(**validated_data)
        already_rsvp = Rsvp.objects.filter(user=rsvp.user, event=rsvp.event).count() > 0
        if already_rsvp:
            raise serializers.ValidationError("You have already confirmed going to this event")

        rsvp.save()
        return rsvp
