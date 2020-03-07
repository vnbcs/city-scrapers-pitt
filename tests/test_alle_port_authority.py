from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.alle_port_authority import AllePortAuthoritySpider

test_response = file_response(
    join(dirname(__file__), "files", "alle_port_authority.html"),
    url="https://www.portauthority.org/inside-Port-Authority/Port-Authority-Board/Board-Meeting-Information/"
)
spider = AllePortAuthoritySpider()

freezer = freeze_time("2020-03-06")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

def test_title():
    assert parsed_items[0]["title"] == "Planning and Stakeholder Relations Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime.datetime(2020, 1, 17, 8, 30)


def test_end():
    assert parsed_items[0]["end"] == None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == 'alle_port_authority/202001170830/x/planning_and_stakeholder_relations_committee'


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Neal H. Holmes Board Room, 5th floor",
        "address": "345 Sixth Avenue, Pittsburgh, PA, 15222"
        }
def test_source():
    assert parsed_items[0]["source"] == "https://www.portauthority.org/inside-Port-Authority/Port-Authority-Board/Board-Meeting-Information/"

def test_links():
    assert parsed_items[0]["links"] == [{
        "href": "",
        "title": ""
        }]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
