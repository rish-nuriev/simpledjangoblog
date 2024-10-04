from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from .models import Article, Category


class ArticlesOnHomePage(ListView):
    model = Article
    template_name = 'blog/articles.html'
    paginate_by = 5

    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        return Article.public_objects.all().select_related(
            'category').prefetch_related('tags')


class ArticlesByCategoryView(ListView):
    model = Article
    template_name = 'blog/articles.html'
    slug_url_kwarg = 'cat_slug'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category,
                                     slug__iexact=self.kwargs.get('cat_slug'))
        context['title'] = category
        return context

    def get_queryset(self):
        return Article.public_objects.filter(
            category__slug=self.kwargs.get('cat_slug')).select_related(
            'category').prefetch_related('tags')


class ArticleDetailView(HitCountDetailView):
    model = Article
    template_name = 'blog/article.html'
    slug_url_kwarg = 'article_slug'
    # set to True to count the hit
    count_hit = True


class ArticlesByTag(ListView):
    template_name = 'blog/articles.html'
    allow_empty = False

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
    #     return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self):
        return Article.public_objects.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("category").prefetch_related('tags')
