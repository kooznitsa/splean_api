from typing import Type

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.serializers import Serializer


def index(request):
    return JsonResponse({'status': 'ok'})


class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializers.get(self.action, self.serializer_class)
