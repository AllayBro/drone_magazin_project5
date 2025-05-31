from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с ролями, никнеймом, аватаром и геоданными.
    """

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')

    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)

    avatar = models.ImageField(
        _('Аватар'),
        upload_to='users/avatars/%Y/%m/%d/',
        null=True,
        blank=True
    )
    nickname = models.CharField(_('Никнейм'), max_length=50, unique=True, blank=True)
    country = models.CharField(_('Страна'), max_length=100, blank=True)
    city = models.CharField(_('Город'), max_length=100, blank=True)
    region = models.CharField(_('Регион'), max_length=100, blank=True)

    role = models.CharField(
        _('Роль'),
        max_length=30,
        choices=Role.choices,
        default=Role.USER
    )

    email_verified = models.BooleanField(_('Email подтвержден'), default=False)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return self.nickname or self.username

    @property
    def full_name(self):
        """Полное имя пользователя"""
        return f'{self.first_name} {self.last_name}'.strip()
