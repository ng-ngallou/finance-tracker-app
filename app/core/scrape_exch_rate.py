import dotenv
import requests  # type: ignore
from bs4 import BeautifulSoup


class ExchangeRate:
    """Scrapes the monthly average exchange rate between CHF and EUR."""

    def __init__(self, month: str, year: str) -> None:
        self.month = month
        self.year = year

        self.soup = self.init_bs()

    def init_bs(self) -> BeautifulSoup:
        dotenv.load_dotenv()
        url = f"https://www.x-rates.com/average/?from=CHF&to=EUR&amount=1&year={self.year}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch data. Status code: {response.status_code}"
            )

        return BeautifulSoup(response.text, "html.parser")

    def find_exch_rate(self) -> float:
        ul = self.soup.find("ul", class_="OutputLinksAvg")
        if not ul:
            raise RuntimeError("Could not find the list of monthly averages")

        for li in ul.find_all("li"):
            month_span = li.find("span", class_="avgMonth")
            rate_span = li.find("span", class_="avgRate")
            if (month_span and rate_span) and month_span.get_text(
                strip=True
            ) == self.month:
                return float(rate_span.get_text(strip=True))

        raise ValueError(f"No rate found for {self.month} {self.year}")
