import abc

from rest_framework import viewsets


@abc.abstractmethod
class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        pass
