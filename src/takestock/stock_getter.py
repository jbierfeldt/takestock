import contextlib
import csv
import urllib


def get_quotes(symbols):
    url = 'http://download.finance.yahoo.com/d/quotes.csv' \
        '?s=' + '+'.join(symbols) + '&f=sl1'
    with contextlib.closing(urllib.urlopen(url)) as response:
        rows = list(csv.reader(response))
    # Make sure we return quotes in the same order as the symbols argument,
    # regardless of the order of Yahoo! results (which we can't guarantee to
    # be in the same order as our request).
    quotes = dict([(symbol, price) for symbol, price in rows])
    return [quotes[symbol] for symbol in symbols]
