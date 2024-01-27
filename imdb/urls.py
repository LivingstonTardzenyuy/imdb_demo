
from django.contrib import admin
from django.urls import path, include 
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('watchlist_app.api.urls')),
    path('account/', include('user_app.api.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name = 'schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # path('api-auth/', include('rest_framework.urls')),  # for login and logout views

]
