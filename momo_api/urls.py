from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter


# Django REST framework API routing
router = DefaultRouter()

# API endpoints
# router.register(r'user-profiles', UserProfileViewSet)

# Construct URLs
urlpatterns = [
    # API registration
    url(r'^api/', include(router.urls)),

    # Django admin views
    url(r'^api-admin/', admin.site.urls),
]


# DEBUG mode only URLs
if settings.DEBUG:
    urlpatterns += [
        # REST framework browsable API login/logout views
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	# API documentation
	# url(r'^api-docs/', include('rest_framework_swagger.urls')),
    ]

    # Media files URL
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
