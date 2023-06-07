"""
URL configuration for bandplanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from bandplannerapi.views import login_user, register_user, BandPhotoView, BandUserView, BundleReleaseView, BundleSongView, EventView, EventTypeView, GigView, MediaContactView, MediaTypeView, NoteView, PressClippingView, RehearsalView, SetlistView, SetlistSongView, SingleReleaseView, SongView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bandphotos', BandPhotoView, 'bandphoto')
router.register(r'bandusers', BandUserView, 'banduser')
router.register(r'bundlereleases', BundleReleaseView, 'bundlerelease')
router.register(r'bundlesongs', BundleSongView, 'bundlesong')
router.register(r'events', EventView, 'event')
router.register(r'eventtypes', EventTypeView, 'eventtype')
router.register(r'gigs', GigView, 'gig')
router.register(r'mediacontacts', MediaContactView, 'mediacontact')
router.register(r'mediatypes', MediaTypeView, 'mediatype')
router.register(r'notes', NoteView, 'note')
router.register(r'pressclippings', PressClippingView, 'pressclipping')
router.register(r'rehearsals', RehearsalView, 'rehearsal')
router.register(r'setlists', SetlistView, 'setlist')
router.register(r'setlistsongs', SetlistSongView, 'setlistsong')
router.register(r'singlereleases', SingleReleaseView, 'singlerelease')
router.register(r'songs', SongView, 'song')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
