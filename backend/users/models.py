from django.contrib.auth.models import AbstractUser, UserManager


class UserQuerySet(UserManager):
    """
    Менеджер пользователя
    """


class User(AbstractUser):
    """
    Пользователь
    """

    objects: UserQuerySet = UserQuerySet()

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
