from django.db import models


from tables.enums import TableRowType


class Table(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TableRow(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TableRowType.choices)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="rows")

    class Meta:
        unique_together = ('title', 'table')
