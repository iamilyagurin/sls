
"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView
from health_check import urls as health_urls

from server.apps.authentication.views import ObtainAuthToken, SignUpView, UserCreateView, UserDetailView
from server.apps.posts import views as post_v
from server.router import CustomRouter

admin.autodiscover()

router = CustomRouter()
# router.register('posts', PostViewSet, basename='post')
# router.register('users', UserViewSet)


api_urlpatterns = [

    path('join/', SignUpView.as_view(), name='sign-up'),
    path('auth-token/', ObtainAuthToken.as_view(), name='auth-token'),
    path('users/', UserCreateView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('media/', post_v.MediaCreate.as_view(), name='media'),
    path('posts/', post_v.PostCreate.as_view(), name='posts'),
    path('posts/<uuid:pk>/', post_v.PostDetail.as_view(), name='post-detail'),
    path('users/<int:user_id>/posts/', post_v.UserPostList.as_view(), name='user-posts'),

]
api_urlpatterns += [path('', router.get_api_root_view(api_urlpatterns))]


urlpatterns = [

    # Health checks:
    path('health/', include(health_urls)),  # noqa: DJ05

    # django-admin:
    path('admin/doc/', include(admindocs_urls)),  # noqa: DJ05
    path('admin/', admin.site.urls),

    # Text and xml static files:
    path('robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path('humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),

    path('api/', include(api_urlpatterns + router.urls))
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
        path('api-auth/', include('rest_framework.urls')),
    ] + urlpatterns + static(
        # Serving media files in development only:
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
