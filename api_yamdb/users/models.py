from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    MAX_EMAIL_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_ROLE_LENGTH,
    MAX_USERS_NAME_LENGTH
)


class Users(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    CHOISES = (
        (ADMIN, "Администратор"),
        (USER, "Аутентифицированный пользователь"),
        (MODERATOR, "Модератор"),
    )

    email = models.EmailField(
        "Электронная почта",
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False
    )

    role = models.CharField(
        "Роль",
        max_length=MAX_ROLE_LENGTH,
        choices=CHOISES, default="user"
    )

    first_name = models.CharField(
        "Имя",
        max_length=MAX_USERS_NAME_LENGTH,
        blank=True,
    )

    last_name = models.CharField(
        "Фамилия",
        max_length=MAX_USERS_NAME_LENGTH,
        blank=True,
    )

    bio = models.TextField(
        "Биография",
        blank=True,
    )

    password = models.CharField(
        blank=True,
        max_length=MAX_PASSWORD_LENGTH
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("role",)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == Users.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == Users.USER
