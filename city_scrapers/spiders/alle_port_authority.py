import dateutil
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AllePortAuthoritySpider(CityScrapersSpider):
    name = "alle_port_authority"
    agency = "Port Authority of Allegheny County"
    timezone = "America/New_York"
    start_urls = [
        "https://www.portauthority.org/inside-Port-Authority/Port-Authority-Board/Board-Meeting-Information/"
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.xpath('/html/body/div[1]/div[4]/div/div/div[1]/table/tbody/tr'):
            if (len(str(item.xpath('td[2]//text()').extract()).split()) > 1):
                meeting = Meeting(
                    title=self._parse_title(item),
                    description=self._parse_description(item),
                    classification=self._parse_classification(item),
                    start=self._parse_start(item),
                    end=self._parse_end(item),
                    all_day=self._parse_all_day(item),
                    time_notes=self._parse_time_notes(item),
                    location=self._parse_location(item),
                    links=self._parse_links(item),
                    source=self._parse_source(response),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting
            else:
                pass

    def _parse_title(self, item):
        """Parse meeting title."""
        return item.xpath('td[1]//text()').extract()[0].strip()

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        day = item.xpath('td[2]//text()').extract()[0].strip()
        time = item.xpath('td[3]//text()').extract()[0].strip()
        timelist = [day, time]
        return dateutil.parser.parse(' '.join(timelist))

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "345 Sixth Avenue, Pittsburgh, PA, 15222",
            "name": "Neal H. Holmes Board Room, 5th floor",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
