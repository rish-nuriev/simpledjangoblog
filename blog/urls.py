from django.urls import path
from . import views

urlpatterns = [
    path('tag/<slug:tag_slug>/', views.ArticlesByTag.as_view(), name='tag'),
    path('<slug:cat_slug>/', views.ArticlesByCategoryView.as_view(),
         name='category'),
    path('<slug:cat_slug>/<slug:article_slug>/', views.ArticleDetailView.as_view(),
         name='article_detail'),
    path('', views.ArticlesOnHomePage.as_view(), name='home'),
]
