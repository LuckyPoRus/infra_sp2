from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import Users
from api_yamdb.settings import MAX_MODELS_NAME_LENGTH, MAX_SLUG_LENGTH

MIN_SCORE = 1
MAX_SCORE = 10


class GenreCategoryBase(models.Model):
    name = models.CharField(
        max_length=MAX_MODELS_NAME_LENGTH
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        abstract = True


class Genre(GenreCategoryBase):

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(GenreCategoryBase):
    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_MODELS_NAME_LENGTH
    )
    year = models.IntegerField(
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="title",
        null=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="genre",
        through="GenreTitle"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
        null=False
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique review"
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
