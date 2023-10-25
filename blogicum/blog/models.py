from django.contrib.auth import get_user_model
from django.db import models

from .constants import CHARACTERS_COUNT


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class CommonInfoBaseModel(models.Model):
    title = models.CharField(
        max_length=CHARACTERS_COUNT,
        verbose_name='Заголовок'
    )

    class Meta:
        abstract = True


class Category(BaseModel, CommonInfoBaseModel):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены '
        'символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=CHARACTERS_COUNT,
        verbose_name='Название места'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(max_length=20, verbose_name='Тег')
    slug = models.SlugField(max_length=20, verbose_name='Слаг')

    class Meta:
        ordering = ('tag',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag


class Post(BaseModel, CommonInfoBaseModel):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в '
        'будущем — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='author_posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='location_posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_posts',
        verbose_name='Категория'
    )
    image = models.ImageField(blank=True,
                              upload_to='posts_images',
                              verbose_name='Картинка')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True,
                                  help_text='''Удерживайте Ctrl
                                  для выбора нескольких вариантов.''')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='Комментируемый пост',
                             related_name='commented_post')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
