from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('box_office/',views.box_office,name='box_office'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('start-scraping/', views.scraping_view, name='scraping_view'),
    path('start-scraping-bo/', views.scraping_boxoffice_view, name='scraping_boxoffice_view'),
    path('model_overview/', views.model_overview, name='model_overview'),


    path('',views.homepage,name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('home_user/',views.home_user,name='home_user'),
]







# Ajoutez cette ligne pour servir les fichiers médias en développement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
