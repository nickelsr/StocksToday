#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import time
from urllib.error import HTTPError, URLError
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        """

        :param master:
        """
        tk.Frame.__init__(self, master)
        self.grid()
        self.outerFrame = None
        self.inputFrame = None
        self.outputFrame = None
        self.closeButton = None
        self.stockEntry = None
        self.stockLabel = None
        self.resultButton = None
        self.resultLabel = None
        self.init_widgets()

    def init_widgets(self):
        self.outerFrame = tk.Frame(self)
        self.inputFrame = tk.Frame(self.outerFrame, bd=4, relief=tk.GROOVE)
        self.outputFrame = tk.Frame(self.outerFrame, bd=4, relief=tk.GROOVE)
        self.closeButton = tk.Button(self, cursor="hand2",
                                     text="Close", command=self.quit)
        self.stockEntry = tk.Entry(self.inputFrame, width=10, justify="center")
        self.stockLabel = tk.Label(self.inputFrame, text="stock symbol")
        self.resultButton = tk.Button(self.inputFrame, cursor="hand2",
                                      text="Submit", command=self.show_prices)
        self.resultLabel = tk.Label(self.outputFrame)
        self.outerFrame.grid()
        self.inputFrame.grid(row=0, column=0)
        self.outputFrame.grid(row=0, column=1)
        self.stockLabel.grid(row=0, column=0)
        self.stockEntry.grid(row=1, column=0)
        self.resultButton.grid(row=2, column=0)
        self.resultLabel.grid()
        self.closeButton.grid()

    def show_prices(self):
        """
        Gets stock ticker input from stock Entry widget,
        instantiate a stock object, then updates result Label widget
        """
        ticker = self.stockEntry.get()
        sq = StockQuery(ticker)
        self._set_result(sq.get_result())

    def _set_result(self, res):
        self.resultLabel.config(text=res)


class StockQuery:
    def __init__(self, ticker):
        """
        Scrapes yahoo finance for data and initializes query result

        :param ticker: stock ticker symbol (e.g., V, for Visa Inc.)
        :type ticker: str
        """
        self._ticker = ticker.upper().strip()
        self._date = date.today().strftime("%b %d, %Y")
        self._company_name = None
        self._open = None
        self._close = None
        self._high = None
        self._low = None
        self.result = None
        self._scrape_page()

    def _scrape_page(self):
        start_time = time.time()
        url = "https://finance.yahoo.com/quote/" + self._ticker + \
              "/history?p=" + self._ticker
        try:
            page = urlopen(url)
            print(time.time() - start_time)
            start_time = time.time()
            page_text = self._get_page_text(page)
            if self._is_valid_ticker(page, url, page_text):
                self._parse_data(page_text)
                print(time.time() - start_time)
        except (HTTPError, URLError) as e:
            self.result = e.reason

    def _get_page_text(self, page):
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup.getText(separator=" ")

    def _is_valid_ticker(self, page, url, page_text):
        not_found = "Requested symbol wasn't found"
        if page.url != url or page_text[0:len(not_found)] == not_found:
            self.result = "(" + self._ticker + ") wasn't found"
            return False
        return True

    def _parse_data(self, page_text):
        price_text = page_text.split(self._date)
        if len(price_text) < 2:  # today's date not found in text
            self.result = "(" + self._ticker + ")" + \
                          " has no price data for " + self._date
            return
        price_text = price_text[1].strip().split(" ")
        self._open = price_text[0]
        self._high = price_text[1]
        self._low = price_text[2]
        self._close = price_text[3]
        self._company_name = page_text.split("(" + self._ticker + ")")[0]
        self._set_prices()

    def _set_prices(self):
        result = self._company_name + "(" + self._ticker + ")\n" + \
                 self._date + "\n\n" + \
                 "High:  " + self._high + "\n" + \
                 "Low:   " + self._low + "\n" + \
                 "Open:  " + self._open + "\n" + \
                 "Close: " + self._close
        self.result = result

    def get_result(self):
        return self.result


app = Application()
app.master.title("Stock Prices from Yahoo Finance")
app.mainloop()
