from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
from urllib.error import HTTPError, URLError
from http.client import InvalidURL


class StockQuery:
    def __init__(self, ticker):
        """
        Scrapes yahoo finance for data and initializes query result

        :param ticker: stock ticker symbol (e.g., V, for Visa Inc.)
        :type ticker: str
        """
        self.ticker = ticker.upper().strip()
        self.date = date.today().strftime("%b %d, %Y")
        self.company_name = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.result = None
        self._scrape_page()

    def _scrape_page(self):
        url = "https://finance.yahoo.com/quote/" + self.ticker + \
              "/history?p=" + self.ticker
        try:
            page = urlopen(url)
            soup = self._get_soup(page)
            page_text = soup.getText(separator=" ")
            if self._is_valid_ticker(page, url, page_text):
                self._parse_data(soup, page_text)
        except (HTTPError, URLError) as e:
            self.result = e.reason
        except InvalidURL:
            self.result = "Invalid stock symbol"

    def _get_soup(self, page):
        html = page.read().decode("utf-8")
        return BeautifulSoup(html, "html.parser")

    def _is_valid_ticker(self, page, url, page_text):
        not_found = "Requested symbol wasn't found"
        if page.url != url or page_text[0:len(not_found)] == not_found:
            self.result = "(" + self.ticker + ") wasn't found"
            return False
        return True

    def _parse_data(self, soup, page_text):
        price_text = page_text.split(self.date)
        if len(price_text) < 2:  # today's date not found in text
            self.result = "(" + self.ticker + ")" + \
                          " has no price data for " + self.date
            return
        price_text = price_text[1].strip().split(" ")
        self.open = price_text[0]
        self.high = price_text[1]
        self.low = price_text[2]
        self.close = price_text[3]
        self.company_name = soup.find("h1").get_text()
        self._set_prices()

    def _set_prices(self):
        result = self.company_name + "\n\n" + \
                 self.date + "\n\n" + \
                 "High:  " + self.high + "\n" + \
                 "Low:   " + self.low + "\n" + \
                 "Open:  " + self.open + "\n" + \
                 "Close: " + self.close
        self.result = result

    def get_result(self):
        """
        Returns string representation of stock query result
        or the appropriate error message

        :return: str
        """
        return self.result
