"""Explorer-related views module."""
import math
from typing import List, Optional

import petl
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView

from explorer.models import Collection
from petl.io.csv_py3 import CSVView
from petl.util.base import DataView

from clients.swapi import SWAPIClient


def index(request: WSGIRequest) -> HttpResponse:
    """Render base.html"""
    return render(request, 'explorer/base.html')


class CollectionListView(ListView):
    """Show list of collections."""
    model = Collection


    def post(self, request:WSGIRequest, *args, **kwargs):
        """Trigger an API fetch."""
        SWAPIClient().fetch_people()
        return redirect('collections')

class CollectionDetailView(DetailView):
    """Show the details of collection."""
    model = Collection
    PAGINATE_BY: int = 10
    TABLE_HEADERS: List[str] = [
        'name', 'height', 'mass',
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "url",
        "date",
    ]
    def get_context_data(self, **kwargs):
        """Add parsed CSV data."""
        context: dict = super().get_context_data(**kwargs)
        table = petl.fromcsv(context['collection'].csv_file)
        total_count: int = petl.nrows(table)

        num_pages: int = math.ceil(total_count / self.PAGINATE_BY)

        page_str: Optional[str] = self.request.GET.get('page')

        curr_page: int
        if page_str:
            curr_page = int(page_str)
        else:
            curr_page = 1


        num_entries: int = curr_page * self.PAGINATE_BY

        context['num_pages'] = num_pages
        context['has_next'] = curr_page < num_pages
        context['curr_page'] = curr_page
        context['next_page'] = curr_page + 1
        context['headers'] = self.TABLE_HEADERS
        context['data'] = petl.head(table, num_entries).data()
        return context


class CollectionValuesDetailView(TemplateView):
    """Show the details of collection alongside with value count in table."""
    model = Collection
    HEADERS: List[str] = [
        'name', 'height', 'mass',
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "url",
        "date",
    ]
    template_name: str = 'explorer/collection_values.html'

    def get_context_data(self, pk, **kwargs):
        """Add all necessary data to the context."""
        context: dict = super().get_context_data(**kwargs)

        context['object'] = get_object_or_404(
            Collection, pk=pk
        )
        context['headers'] = self.HEADERS

        group_by_str = self.request.GET.get('values', "")
        group_by: List[str] = group_by_str.split(',')
        if not group_by_str:
            context['data'] = {}
        else:
            context['table_headers'] = [*group_by, 'count']
            table: CSVView = petl.fromcsv(context['object'].csv_file)
            data: DataView = petl.valuecounts(table, *group_by).cutout('frequency').data()
            context['data'] = data
        return context
