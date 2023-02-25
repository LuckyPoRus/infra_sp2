from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username, validate_year
from users.models import Users
from api_yamdb.settings import MAX_EMAIL_LENGTH, MAX_USERS_NAME_LENGTH


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        validators=(validate_year,)
    )

    class Meta:
        fields = (
            "id", "name", "year", "description", "genre", "category",
        )
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category",
        )
        read_only_fields = fields
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date",)
        model = Review

    def validate(self, data):
        request = self.context["request"]
        title = get_object_or_404(
            Title,
            pk=self.context["view"].kwargs.get("title_id")
        )
        if (
            Review.objects.filter(title=title, author=request.user).exists()
            and request.method == "POST"
        ):
            raise serializers.ValidationError(
                "Вы уже оставили озыв на это произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            validate_username,
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=Users.objects.all())
        ),
        max_length=MAX_USERS_NAME_LENGTH,
        allow_blank=False,
        required=True
    )

    class Meta:
        abstract = True
        model = Users
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH
    )
    username = serializers.CharField(
        required=True,
        validators=(
            UnicodeUsernameValidator(),
            validate_username
        ),
        max_length=MAX_USERS_NAME_LENGTH
    )


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена при регистрации."""

    username = serializers.CharField(
        required=True,
        validators=(
            UnicodeUsernameValidator(),
            validate_username
        )
    )
    confirmation_code = serializers.CharField(required=True)


class IsntAdminSerializer(UsersSerializer):

    class Meta(UsersSerializer.Meta):
        read_only_fields = ("role",)
