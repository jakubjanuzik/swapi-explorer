"""Star Wars API client module."""
import uuid
from datetime import datetime
from typing import Optional

import requests
from django.core.files import File
from petl.io.json import DictsView
from requests import Response
from dateutil import parser
from explorer.models import Homeworld, Collection
import petl
import csv


class SWAPIClient:
    """Stars Wars API Client used to fetch data."""
    BASE_URL: str = 'https://swapi.dev'
    DATE_FORMAT: str = '%Y-%m-%d'
    FILENAME_DATE_FORMAT: str = "%a %d, %Y, %I:%m %p"
    FIELDS_TO_DROP = ['films', 'vehicles', 'starships', 'created', 'species', 'edited']

    def _fetch_homeworld(self, homeworld_url: str) -> str:
        """Fetch homeworld from API.

        Note: homeworld returns residents data. Perhaps this could be useful."""
        response: Response = requests.get(homeworld_url)

        response.raise_for_status()

        return response.json()['name']


    def _get_homeworld_str(self, homeworld_url: str) -> str:
        """Fetch homeworld from database, if non-existent then fetch from API
        and save to the database."""
        homeworld: Optional[Homeworld] = Homeworld.objects.filter(url=homeworld_url).first()
        if homeworld is not None:
            return homeworld.name

        try:
            homeworld_name: str = self._fetch_homeworld(homeworld_url)
        except requests.HTTPError:
            #  TODO: Add logging
            return ""

        Homeworld.objects.create(url=homeworld_url, name=homeworld_name)
        return homeworld_name


    def _convert_create_to_date(self, created_at: str) -> str:
        """Covert ISO 8601 string to date format specified in DATE_FORMAT attribute."""
        parsed_date: datetime = parser.parse(created_at)
        return datetime.strftime(parsed_date, self.DATE_FORMAT)

    def _get_people_data(self, response: Response) -> list:
        """Return people data response has been successful."""

        try:
            response.raise_for_status()
        except requests.HTTPError:
            #  TODO: Add logger and log the failure
            return []

        data: list = response.json()['results']
        person_data: dict
        for person_data in data:
            person_data['date'] = self._convert_create_to_date(
                person_data['created']
            )
            person_data['homeworld'] = self._get_homeworld_str(person_data['homeworld'])
            field: str
            for field in self.FIELDS_TO_DROP:
                person_data.pop(field, None)
        return data

    def _save_to_csv(self, people_data: list) -> None:
        """Save people data to CSV files in 'files/' folder.

        Also create a Collection object in database."""
        filename: str = f"files/{uuid.uuid4().hex}.csv"
        table: DictsView = petl.fromdicts(people_data)
        petl.tocsv(table, filename)

        with open(filename) as fp:
            Collection.objects.create(csv_file=File(fp))

    def fetch_people(self) -> None:
        """Fetch people using /api/people endpoint and save contents to the
        CSV file.
        """
        url: str = f"{self.BASE_URL}/api/people/"
        people_data: list = []

        response: Response = requests.get(url)
        people_data.extend(self._get_people_data(response))

        next_url: str = response.json()['next']
        while next_url:
            response: Response = requests.get(next_url)

            people_data.extend(self._get_people_data(response))
            next_url: str = response.json()['next']

        self._save_to_csv(people_data)



