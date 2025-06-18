from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('apps.users.urls')),
    path('api/border-crosses/', include('apps.border.urls')),
    path('api/migrants/', include('apps.migrant.urls')),
    path('api/chart/', include('apps.chart.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
else:
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')),
        path('api/schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
        path('docs/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    ]
