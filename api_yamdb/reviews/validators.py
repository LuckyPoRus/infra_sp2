import datetime

from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == "me":
        raise ValidationError(
            'Имя пользователя "me" недопустимо.' "Измените имя!"
        )


def validate_year(value):
    year = datetime.datetime.now().year
    if value > year:
        raise ValidationError(
            'Указанный год больше текущего!'
        )
    return value
