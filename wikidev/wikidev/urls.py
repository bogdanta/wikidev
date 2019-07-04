from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search_wizard', views.SearchWizardView.as_view(), name='search_wizard'),
    path('random', views.RandomView.as_view(), name='random'),
    path('language', views.LanguageView.as_view(), name='language'),
]

