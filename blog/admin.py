from django import forms
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Category, TagPost


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = "__all__"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "category", "is_published", "tag_list")
    exclude = ("slug",)
    list_editable = ("is_published",)
    list_filter = ("category",)
    filter_horizontal = ["tags"]
    # filter_vertical = ['tags']
    search_fields = ("title", "content")

    def get_queryset(self, request):
        qs = self.model.objects.get_queryset()

        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.prefetch_related("tags")

    def tag_list(self, obj):
        return list(obj.tags.all())

    tag_list.short_description = "Теги"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )
    exclude = ["slug"]


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ("tag", "slug")
    prepopulated_fields = {"slug": ("tag",)}
    search_fields = ("tag", "slug")
