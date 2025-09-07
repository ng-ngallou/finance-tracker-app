import pytest
from bs4 import BeautifulSoup
import requests

from finance_tracker_app.core.scrape_exch_rate import ExchangeRate


@pytest.fixture
def fake_html():
    # Minimal HTML snippet
    return """
    <html>
        <body>
            <ul class="OutputLinksAvg">
                <li>
                    <span class="avgMonth">Jan</span>
                    <span class="avgRate">0.96</span>
                </li>
                <li>
                    <span class="avgMonth">Feb</span>
                    <span class="avgRate">0.97</span>
                </li>
            </ul>
        </body>
    </html>
    """


def test_find_exch_rate(monkeypatch, fake_html):
    """Test that ExchangeRate.find_exch_rate returns the correct value."""

    class DummyResponse:
        status_code = 200
        text = fake_html

    def mock_get(url, headers):
        return DummyResponse()

    # Patch requests.get so no real network call happens
    monkeypatch.setattr(requests, "get", mock_get)

    exch = ExchangeRate(month="Feb", year="2025")
    rate = exch.find_exch_rate()

    assert isinstance(rate, float)
    assert rate == 0.97


def test_find_exch_rate_not_found(monkeypatch, fake_html):
    """Test that ValueError is raised if the month is not in the HTML."""

    class DummyResponse:
        status_code = 200
        text = fake_html

    monkeypatch.setattr(requests, "get", lambda *_, **__: DummyResponse())

    exch = ExchangeRate(month="March", year="2025")

    with pytest.raises(ValueError):
        exch.find_exch_rate()


def test_init_bs_failure(monkeypatch):
    class DummyResponse:
        status_code = 500
        text = "Error"

    monkeypatch.setattr(requests, "get", lambda *_, **__: DummyResponse())

    with pytest.raises(Exception, match="Failed to fetch data"):
        ExchangeRate(month="January", year="2025")

