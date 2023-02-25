from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, Users
from api_yamdb.settings import MESSAGE_EMAIL_EXISTS, MESSAGE_USERNAME_EXISTS
from .filters import FilterTitle
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdminOnly,
    IsAdminOrReadOnly,
    IsAuthorOrModerOrAdminOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UsersSerializer
)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = FilterTitle
    ordering_fields = ["rating", "category", "genre"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerOrAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "head", "patch", "delete"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path="me",
        url_name="me",
    )
    def info_about_user(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    """Функция получения токена при регистрации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    user = get_object_or_404(Users, username=username)
    confirmation_code = serializer.validated_data.get(
        "confirmation_code"
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return response.Response(
            {"token": str(token)},
            status=status.HTTP_200_OK
        )
    return response.Response(
        {"confirmation_code": "Неверный код подтверждения!"},
        status=status.HTTP_400_BAD_REQUEST
    )


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    @staticmethod
    def send_email(data):
        email = EmailMessage(body=data["email_body"], to=[data["to_email"]])
        email.send()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            user, _ = Users.objects.get_or_create(
                username=serializer.validated_data.get("username"),
                email=serializer.validated_data.get("email")
            )
        except IntegrityError:
            return response.Response(
                MESSAGE_EMAIL_EXISTS if
                Users.objects.filter(username="username").exists()
                else MESSAGE_USERNAME_EXISTS,
                status.HTTP_400_BAD_REQUEST
            )

        code = default_token_generator.make_token(user)
        data = {
            "email_body": f"{user.username}, {code}",
            "to_email": user.email,
        }
        self.send_email(data)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )
