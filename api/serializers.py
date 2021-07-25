from rest_framework import serializers
from image_parser.models import TableFromImage, TableRowFromImage, TableCellFromImage


class TableCellFromImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCellFromImage
        fields = ['column', 'text', 'image', 'processed_image']


class TableRowFromImageSerializer(serializers.ModelSerializer):
    table_cells = TableCellFromImageSerializer(many=True, read_only=True)

    class Meta:
        model = TableRowFromImage
        fields = ['row', 'table_cells']


class TableFromImageSerializer(serializers.ModelSerializer):
    table_rows = TableRowFromImageSerializer(many=True, read_only=True)

    class Meta:
        model = TableFromImage
        fields = ['id', 'total_columns', 'total_rows', 'table_rows']
        depth = 4
