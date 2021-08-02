import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import VerifiedTableCell

from .serializers import TableFromImage
from .serializers import (TableFromImageSerializer,
                          VerifiedTableDataSerializer)


# Create your views here.
@api_view(['GET'])
def api_status(request):
    status = {'status': 'Running'}
    return Response(status)


@api_view(['GET'])
def table_data_list(request, table_id):
    table = TableFromImage.objects.get(id=table_id)
    if not table.verified_cells.all().exists():
        for row in table.table_rows.all():
            for cell in row.table_cells.all():
                verified_table_cell = VerifiedTableCell(table=table)
                verified_table_cell.column = cell.column
                verified_table_cell.row = row.row
                verified_table_cell.text = cell.text
                verified_table_cell.image = cell.image
                verified_table_cell.save()

    serializer = VerifiedTableDataSerializer(instance=table)
    return Response(serializer.data)


@api_view(['POST'])
def update_verified_table_data(request):
    table = TableFromImage.objects.get(pk=request.data.get('id'))
    serializer = VerifiedTableDataSerializer(instance=table, data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(serializer.data)
