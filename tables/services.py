from __future__ import annotations

from typing import Any

from django.apps import apps
from django.db import connection
from django.db import models

from dynamic_tables.settings import FIELD_TYPES, MODULE_NAME
from tables.models import Table, TableRow


def create_model(
        name: str,
        fields: dict[str, Any] | None = None,
        module: str = "",
) -> models.Model:
    class Meta:
        app_label = module

    attributes = {"__module__": module, "meta": Meta}

    if fields:
        attributes.update(fields)

    model: type[models.Model] = type(name, (models.Model,), attributes)

    return model


def save_model(model: models.Model, module: str):
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)

    apps.register_model(module, model)


def add_field_to_model(model: models.Model, field: dict[str, models.Field]) -> models.Model:
    with connection.schema_editor() as schema_editor:
        schema_editor.add_field(model, field)
    return model


def rename_model(model: models.Model, old_name: str, new_name: str, module: str):
    with connection.schema_editor() as schema_editor:
        schema_editor.alter_db_table(model, f"{module}_{old_name}", f"{module}_{new_name}")


def get_model(table: Table) -> models.Model:
    fields = {}
    for row in table.rows.all():
        fields[row.title] = FIELD_TYPES[row.type]

    return create_model(table.name, fields, MODULE_NAME)


def get_element_by_key(elements: list[dict[str, Any]], key: str, value: Any) -> Any:
    for element in elements:
        if element[key] == value:
            return element
    return None
