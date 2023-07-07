from django.db import models


class TableRowType(models.TextChoices):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
