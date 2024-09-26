from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35, verbose_name="телефон", help_text="Укажите телефон", **NULLABLE
    )

    city = models.CharField(
        max_length=50, verbose_name="город", help_text="Укажите город", **NULLABLE
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        help_text="Загрузите аватар",
        **NULLABLE,
    )

    tg_chat_id = models.CharField(max_length=50,
                                  verbose_name='телеграм chat-id',
                                  help_text='Укажите телеграм chat-id',
                                  **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
