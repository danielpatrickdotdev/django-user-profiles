from django.conf.urls import *
from django.views.generic import DetailView
from profiles.models import CustomUser

urlpatterns = patterns('',
    url(r'^(?P<username>[\w-]+)/$',
        DetailView.as_view(
            model=CustomUser,
            slug_field='username',
            slug_url_kwarg='username',
            context_object_name='profile',
            template_name='profiles/detail.html'),
        name='user_detail'),
)
