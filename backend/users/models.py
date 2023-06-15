import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# В валидаторы не переносить, иначе круговой импорт
def validate_username(data):
    if data == 'me':
        raise ValidationError(
            'Имя "me" зарезервировано, используйте другое'
        )
    if not re.search(r'^[\w.@+-]+\Z', data):
        raise ValidationError(
            'В имени пользователя использованы недопустимые символы')
    return data


class User(AbstractUser):
    """Кастомная модель юзера."""

    username = models.CharField('Ник пользователя',
                                max_length=150,
                                blank=False,
                                null=False,
                                unique=True,
                                validators=[validate_username])
    email = models.EmailField('Электронная почта',
                              max_length=254,
                              blank=False,
                              null=False,
                              unique=True)
    first_name = models.CharField('Имя пользователя',
                                  max_length=150,
                                  blank=False,
                                  null=False)
    last_name = models.CharField('Фамилия пользователя',
                                 max_length=150,
                                 blank=False,
                                 null=False)
    password = models.CharField('Пароль',
                                max_length=150,
                                blank=False,
                                null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_constraint'
            ),
        ]

    def __str__(self):
        return f'{self.username} - {self.email}'


class Follow(models.Model):
    """Модель подписки на других пользователей."""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['author', 'user'],
                                    name='unique following')
        ]
