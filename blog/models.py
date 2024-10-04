import random
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from hitcount.models import HitCount


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(is_published=True)


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name="Заголовок", unique=True)
    slug = models.SlugField(max_length=256)
    content = models.TextField(blank=True, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(
        upload_to="photo/%Y/%m/%d/", blank=True, verbose_name="Фото"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="articles",
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="tags", verbose_name="Теги"
    )

    objects = models.Manager()
    public_objects = ArticleManager()

    def get_absolute_url(self):
        return reverse(
            "article_detail",
            kwargs={"cat_slug": self.category.slug, "article_slug": self.slug},
        )

    def get_photo_url(self):
        """
        Our articles don't require images.
        But to prevent errors we have to define some default image here
        """
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        else:
            return "/static/img/default.png"

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    @classmethod
    def get_random_tags(cls, tags_number=5):
        # Джанго позволяет получить случайные записи
        # вот так - cls.objects.order_by("?")[:tags_number]
        # но в случае увеличения кол-ва тегов в БД
        # нагрузка на БД будет возрастать
        # поэтому лучше использовать random
        all_tags = list(cls.objects.all())
        random.shuffle(all_tags)

        return all_tags[:tags_number]
