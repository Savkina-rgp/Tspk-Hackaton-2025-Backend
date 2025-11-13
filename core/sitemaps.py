from django.contrib.sitemaps import GenericSitemap

from core.models.bases import BaseRenderableModel
from shared.reflection import get_subclasses


# На случай, если нужен будет кастомный Sitemap для модели
_EXCLUDED_MODELS: set = set()

# Если какая-то запись будет не нужна в Sitemap - её исключат в
# robots.txt через disallow
def get_base_renderables_sitemaps() -> dict[str, GenericSitemap]:
	return {
		model._meta.model_name: GenericSitemap({
			'queryset': model.objects.order_by('-last_modified_time'),
			'date_field': 'last_modified_time'
		})
		for model in get_subclasses(BaseRenderableModel)
		if not model._meta.abstract and model not in _EXCLUDED_MODELS
	}
