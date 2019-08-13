from bs4 import BeautifulSoup
from bom_scraper import bom_metadata
import logging

logger = logging.getLogger()

with open("tests/test_data.html") as fp:
    test_data = fp.read()

soup = BeautifulSoup(test_data)


def test_get_div_text():
    logger.info("Test getting div text")
    assert bom_metadata.get_div_text(
        "Release\xa0Dates:\n\xa0September 14, 2012 (limited)\n\xa0September 21, 2012 (wide)\n"
    ) == ["ReleaseDates:", "September 14, 2012 (limited)", "September 21, 2012 (wide)"]


def test_process_grosses():
    logger.info("Test getting grosses")
    gross_data = soup.find("div", {"id": "grosses"})
    assert bom_metadata.process_grosses(gross_data) == (
        "$16,377,274",
        "$11,880,786",
        "$28,258,060",
    )
