from core.views.bases 	import BaseRenderableDetailView, PageBasedListView
from business 			import models


# MARK: Article
class ArticleListView(PageBasedListView):
	renderable_slug = 'blog'
	queryset = models.Article.objects.published()

class ArticleDetailView(BaseRenderableDetailView):
	queryset = models.Article.objects.published()


# MARK: Service
# class ServiceListView(PageBasedListView):
# 	renderable_slug = 'services'
# 	queryset = models.Service.objects.all()

# class ServiceDetailView(BaseRenderableDetailView):
# 	model = models.Service
