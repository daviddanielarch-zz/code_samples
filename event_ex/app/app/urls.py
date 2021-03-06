"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from events.views import EventsAPI, RsvpAPI, EventDetail, home, create_event
from custom_auth.views import CustomLoginView, SignupView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/events', EventsAPI, basename='events')
router.register(r'api/rsvp', RsvpAPI, basename='rsvp')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^accounts/signup/$', SignupView.as_view(), name='signup'),
    url(r'^accounts/login/$', CustomLoginView.as_view(), name='login'),
    url(r'^event_detail/(?P<pk>[^/.]+)/$', EventDetail.as_view()),
    url(r'^event_create/$', create_event, name='create-event')
]
urlpatterns += router.urls

