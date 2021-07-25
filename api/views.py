from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import  TableFromImage
from .serializers import (TableFromImageSerializer)

# Create your views here.
@api_view(['GET'])
def api_status(request):
    status = { 'status':'Running'}
    return Response(status)

@api_view(['GET'])
def table_data_list(request):
    table = TableFromImage.objects.all().last()
    serializer = TableFromImageSerializer(instance=table)
    return Response(serializer.data)


@api_view(['POST'])
def update_table_data(request):
    serializer = TableFromImageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)