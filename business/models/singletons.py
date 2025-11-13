from django.db import models
from solo.models import SingletonModel


class BusinessConfig(SingletonModel):
	saplings_in_hectare = models.PositiveSmallIntegerField(default = 1000,
		help_text='Используется в калькуляторе стоимости')

	class Meta:
		verbose_name = '🛠 | Конфиг бизнес параметров'
