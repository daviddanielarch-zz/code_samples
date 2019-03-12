from django.contrib.auth.views import LoginView
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from events.models import Event, Rsvp
from events.pagination import NormalPagination
from events.permissions import IsOwner
from events.serializers import EventSerializer, RsvpSerializer


class EventDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event_detail.html'

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response({'serializer': serializer, 'event': event})


class EventsAPI(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = NormalPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


class RsvpAPI(viewsets.ModelViewSet):
    queryset = Rsvp.objects.all()
    serializer_class = RsvpSerializer


def home(request):
    return render(request, 'list.html')


def create_event(request):
    return render(request, 'create.html')
