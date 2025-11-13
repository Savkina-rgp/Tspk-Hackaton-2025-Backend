from django.db import models
from core.models.bases import OrderedModel, UniqueNamedModel

# Пока под вопросом, будет ли у услуги List & Detail страницы
class Service(UniqueNamedModel, OrderedModel):
	summary = models.TextField('Краткое описание', max_length=256)

	class Meta(OrderedModel.Meta):
		verbose_name_plural = 'услуга'
		verbose_name = 'услуги'
