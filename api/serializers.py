from rest_framework import serializers
from image_parser.models import (TableFromImage,
                                 TableRowFromImage,
                                 TableCellFromImage)
from .models import VerifiedTableCell


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
        fields = ['id', 'total_columns', 'total_rows', 'table_rows', 'telegram_media']
        depth = 2


class VerifiedTableCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedTableCell
        fields = ['table', 'row', 'column', 'text', 'image']
        # read_only_fields = ['table', 'row', 'column', 'image']


class VerifiedTableDataSerializer(serializers.ModelSerializer):
    verified_cells = VerifiedTableCellSerializer(many=True)

    class Meta:
        model = TableFromImage
        fields = ['id', 'total_rows', 'total_columns', 'verified_cells']
        depth = 2

    def update(self, instance, validated_data):
        verified_cells = validated_data.pop('verified_cells')
        for cell in verified_cells:
            cell_obj = VerifiedTableCell.objects.get(table=instance, row=cell.get('row'), column=cell.get('column'))
            if cell_obj.text == cell.get('text'):
                continue
            print(cell_obj.row, cell_obj.column, "modified")
            cell_obj.text = cell.get('text')
            cell_obj.save()
        return instance;
