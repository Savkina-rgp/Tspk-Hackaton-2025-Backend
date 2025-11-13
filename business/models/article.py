from typing import Callable, Self

from django.utils 	import timezone
from django.db 		import models

from tinymce.models import HTMLField

from core.models.bases import BaseRenderableModel


class ArticleQuerySet(models.QuerySet):
	def published(self):
		return self.filter(publish_date__lte = timezone.now())

class ArticleManager(models.manager.BaseManager.from_queryset(ArticleQuerySet)):
	published: Callable[[Self], Self]

class Article(BaseRenderableModel):
	image = models.ImageField(upload_to = 'articles')
	content = HTMLField('Содержимое')
	publish_date = models.DateTimeField('Дата публикации', default = timezone.now,
		help_text='Статьи, чья дата публикации ещё не наступила, не будут отображаться на сайте')

	objects: ArticleManager = ArticleManager()

	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'

	@property
	def is_published(self):
		return self.publish_date <= timezone.now()
