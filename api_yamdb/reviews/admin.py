from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "slug",
        )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]


class GenreTitleResource(resources.ModelResource):
    genre_id = Field(attribute="genre_id", column_name="genre_id")
    title_id = Field(attribute="title_id", column_name="title_id")

    class Meta:
        model = GenreTitle
        fields = (
            "id",
            "genre_id",
            "title_id",
        )


class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]


class TitleResource(resources.ModelResource):
    category_id = Field(attribute="category_id", column_name="category_id")

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category_id",
        )


class TitleAdmin(ImportExportModelAdmin):
    from_encoding = "utf-8-sig"
    resource_classes = [TitleResource]


class ReviewResource(resources.ModelResource):
    title_id = Field(attribute="title_id", column_name="title_id")
    csv_pub_date = Field(attribute="pub_date", column_name="pub_date")

    class Meta:
        model = Review
        fields = (
            "id",
            "title_id",
            "text",
            "score",
            "author",
            "csv_pub_date",
        )


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]


class CommentResource(resources.ModelResource):
    review_id = Field(attribute="review_id", column_name="review_id")
    author_id = Field(attribute="author_id", column_name="author_id")
    csv_pub_date = Field(attribute="pub_date", column_name="pub_date")

    class Meta:
        model = Comment
        fields = (
            "id",
            "review_id",
            "text",
            "author_id",
            "csv_pub_date",
        )


class CommentAdmin(ImportExportModelAdmin):
    from_encoding = "utf-8-sig"
    resource_classes = [CommentResource]


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
