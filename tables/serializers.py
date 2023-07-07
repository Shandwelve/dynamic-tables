from typing import Any

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dynamic_tables.settings import FIELD_TYPES, MODULE_NAME
from tables.enums import TableRowType
from tables.models import Table, TableRow
from tables.services import create_model, get_model, add_field_to_model, save_model, rename_model, get_element_by_key


class TableRowSerializer(serializers.ModelSerializer[TableRow]):
    title = serializers.CharField(min_length=3, max_length=255)
    type = serializers.ChoiceField(choices=TableRowType.choices)

    def create(self, validated_data: dict[str, Any]) -> TableRow:
        model = get_model(validated_data["table"])
        field = FIELD_TYPES[validated_data["type"]]
        field.column = validated_data["title"]
        add_field_to_model(model, field)

        return super().create(validated_data)

    class Meta:
        model = TableRow
        fields = ("title", "type")


class TableSerializer(serializers.ModelSerializer[Table]):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        min_length=3,
        max_length=255,
        validators=[UniqueValidator(queryset=Table.objects.all())],
    )
    rows = TableRowSerializer(many=True)

    def create(self, validated_data: dict[str, Any]) -> Table:
        rows = []

        if "rows" in validated_data:
            rows = validated_data.pop("rows")

        table = super().create(validated_data)

        fields = {}

        for row in rows:
            table_row = TableRow.objects.create(table=table, **row)
            fields[table_row.title] = FIELD_TYPES[table_row.type]

        model = create_model(name=table.name, fields=fields, module=MODULE_NAME)
        save_model(model, MODULE_NAME)

        return table

    def update(self, instance: Table, validated_data: dict[str, Any]) -> Table:
        instance.rows.all().delete()
        for row in validated_data.pop("rows"):
            TableRow.objects.create(table=instance, **row)

        rename_model(instance, instance.name, validated_data["name"], MODULE_NAME)

        return super().update(instance, validated_data)

    class Meta:
        model = Table
        fields = ("id", "name", "rows")
