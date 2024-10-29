from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from .models import EquityRecord
from .serializers import EquityRecordSerializer

def home_view(request):
    return HttpResponse("<h1>Welcome to the Bhavcopy API!</h1>")


# Viewset for CRUD operations on EquityRecord
class EquityRecordViewSet(viewsets.ModelViewSet):
    queryset = EquityRecord.objects.all()
    serializer_class = EquityRecordSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            equity_record = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(equity_record)
            return Response(serializer.data)
        except EquityRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            equity_record = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(equity_record, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EquityRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            equity_record = self.get_queryset().get(pk=pk)
            equity_record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EquityRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
