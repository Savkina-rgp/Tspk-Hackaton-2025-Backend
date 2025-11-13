from decimal import Decimal

from rest_framework.decorators 	import action
from rest_framework.generics 	import get_object_or_404
from rest_framework.response 	import Response
from rest_framework.request 	import Request
from rest_framework 			import status, viewsets

from business.api.serializers 	import SaplingsCalculatorSerializer
from business.models 			import HectarePatronage, BusinessConfig


class SaplingsCalculatorViewSet(viewsets.ViewSet):
	serializer_class = SaplingsCalculatorSerializer

	@action(detail=True, methods=['POST'])
	def calculate(self, request: Request, slug: str) -> Response:
		tariff = get_object_or_404(HectarePatronage, slug=slug)

		serializer = SaplingsCalculatorSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		price = self._calculate_price(tariff, serializer.validated_data['saplings'])
		return Response({"price": price}, status=status.HTTP_200_OK)

	def _calculate_price(lot: HectarePatronage, saplings_count: int):
		hectare_price = Decimal(lot.price) / Decimal(lot.hectares)
		sapling_price = hectare_price / BusinessConfig.get_solo().saplings_in_hectare

		return sapling_price * saplings_count
