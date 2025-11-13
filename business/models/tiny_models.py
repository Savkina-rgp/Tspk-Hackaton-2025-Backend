from django.db import models
from core.models.bases import OrderedModel, UniqueNamedModel

class HowItsWorkItem(OrderedModel):
	text = models.CharField('Текст', max_length=128)

	class Meta(OrderedModel.Meta):
		verbose_name = 'элемент "Как это работает"'
		verbose_name_plural = 'элементы "Как это работает"'

	def __str__(self):
		return f"{self.order:02d}. {self.text.upper()}"

class Parthners(UniqueNamedModel, OrderedModel):
	svg_code = models.TextField('SVG Код')

	class Meta(OrderedModel.Meta):
		verbose_name = 'партнёр'
		verbose_name_plural = 'партнёры'
