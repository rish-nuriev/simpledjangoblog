from django import template
from django.db.models import Count, F

from blog.models import Category, Article, TagPost

register = template.Library()


#
# @register.simple_tag(name="cat_list")
# def get_categories():
#     return Category.objects.all()


@register.inclusion_tag("blog/list_categories.html")
def show_categories():
    categories = (
        Category.objects.annotate(
            cnt=Count("articles", filter=F("articles__is_published"))
        )
        .filter(cnt__gt=0)
        .order_by("-cnt")
    )
    return {"categories": categories}


@register.inclusion_tag("blog/popular_articles.html")
def show_popular_articles():
    articles = Article.public_objects.order_by("-hit_count_generic__hits")[
        :3
    ].select_related("category")
    return {"articles": articles}


@register.inclusion_tag("blog/similar_articles.html")
def show_similar_articles(article):
    # Список схожих постов
    articles_tags_ids = article.tags.values_list("id", flat=True)
    similar_articles = Article.public_objects.filter(tags__in=articles_tags_ids).exclude(
        id=article.id
    )
    similar_articles = similar_articles.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-created_at"
    )[:4]
    return {"similar_articles": similar_articles}


@register.inclusion_tag("blog/sidebar_tags.html")
def show_tags_in_sidebar():
    ten_tags = TagPost.get_random_tags(10)
    return {"ten_tags": ten_tags}
