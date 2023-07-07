from __future__ import annotations

from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, status

from tables.models import Table, TableRow
from tables.serializers import TableSerializer, TableRowSerializer


class DynamicTablesViewSet(viewsets.GenericViewSet):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    pagination_class = None

    def list(self, request: Request) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk: int | None = None) -> Response:
        table = self.get_object()
        serializer = self.get_serializer(table)

        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request: Request, pk: int | None = None) -> Response:
        table = self.get_object()
        serializer = self.get_serializer(table, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DynamicTableRowsViewSet(viewsets.GenericViewSet):
    serializer_class = TableRowSerializer
    queryset = TableRow.objects.all()
    pagination_class = None

    def list(self, request: Request, table_pk: int | None = None) -> Response:
        table_rows = self.queryset.filter(table=table_pk)
        serializer = self.get_serializer(table_rows, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request, table_pk: int | None = None) -> Response:
        table = get_object_or_404(Table.objects.all(), pk=table_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(table=table)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
