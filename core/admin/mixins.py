class DynamicExtraMixin:
	def get_extra(self, request, obj = None, **kwargs):
		extra: int = super().get_extra(request, obj, **kwargs)
		return extra if obj is None else 0
