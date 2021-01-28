import tkinter as tk
from stock_query import StockQuery


class Application(tk.Frame):
    def __init__(self, master=None):
        """Create widgets, assemble layout, assign functionality"""
        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.winfo_geometry()
        self.outerFrame = None
        self.inputFrame = None
        self.outputFrame = None
        self.closeButton = None
        self.stockEntry = None
        self.stockLabel = None
        self.resultButton = None
        self.resultText = None
        self._init_widgets()

    def _init_widgets(self):
        self.inputFrame = tk.Frame(self)
        self.outputFrame = tk.Frame(self, relief=tk.GROOVE)
        self.stockEntry = tk.Entry(self.inputFrame, width=10, justify="center")
        self.stockLabel = tk.Label(self.inputFrame, text="Stock Tick Symbol")
        self.resultButton = tk.Button(self.inputFrame, cursor="hand2",
                                      text="Submit", command=self._show_prices)
        self.resultText = tk.Text(self.outputFrame, width=20, height=10,
                                  wrap="word", state="disabled")
        self.inputFrame.grid(row=0, column=0, sticky="nsew", pady=10)
        self.outputFrame.grid(row=1, column=0, padx=1, sticky="nsew")
        self.stockLabel.grid(row=0, column=0)
        self.stockEntry.grid(row=1, column=0, sticky="nsew")
        self.resultButton.grid(row=1, column=1, sticky="SW", padx=3)
        self.resultText.grid(sticky="nsew")
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.outputFrame.rowconfigure(0, weight=1)
        self.outputFrame.columnconfigure(0, weight=1)
        self.resultText.rowconfigure(0, weight=1)
        self.resultText.columnconfigure(0, weight=1)

    def _show_prices(self):
        ticker = self.stockEntry.get()
        sq = StockQuery(ticker)
        self._set_result(sq.get_result())

    def _set_result(self, res):
        self.resultText.config(state="normal")
        self.resultText.delete(1.0, tk.END)
        self.resultText.insert(tk.END, res)
        self.resultText.config(state="disabled")
