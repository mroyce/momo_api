from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from momo_api.account.views import CompanyProfileViewSet, UserProfileViewSet
from momo_api.base.auth.jwt import JWTLoginView, JWTSignUpView
from momo_api.listing.views import EventViewSet, ListingViewSet


# Django REST framework API routing
router = DefaultRouter()

# API endpoints
# account
router.register(r'users', UserProfileViewSet)
router.register(r'companies', CompanyProfileViewSet)

# listing
router.register(r'events', EventViewSet)
router.register(r'listings', ListingViewSet)

# Construct URLs
urlpatterns = [
    # API registration
    url(r'^api/', include(router.urls)),

    # Django admin views
    url(r'^api-admin/', admin.site.urls),

    # API Authentication
    url(r'^api/auth/sign-up/', JWTSignUpView.as_view(), name='sign-up'),
    url(r'^api/auth/login/', JWTLoginView.as_view(), name='login'),
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
