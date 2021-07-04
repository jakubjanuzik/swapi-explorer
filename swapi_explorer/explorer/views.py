"""Explorer-related views module."""
import math
from typing import Optional

import petl
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from explorer.models import Collection


def index(request: WSGIRequest) -> HttpResponse:
    """Render base.html"""
    return render(request, 'explorer/base.html')


class CollectionListView(ListView):
    """Show list of collections."""
    model = Collection



class CollectionDetailView(DetailView):
    """Show the details of collection."""
    model = Collection
    PAGINATE_BY: int = 10
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
        context['data'] = petl.head(table, num_entries).data()
        context['curr_page'] = curr_page
        context['next_page'] = curr_page + 1
        context['headers'] = [
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
        return context

