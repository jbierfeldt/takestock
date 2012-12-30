import re
import urllib

def get_quote(symbol):
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    find_q = re.search(r'\<span\sid="ref_\d+.*">(.+)<', content)
    return find_q.group(1) if find_q else 'no quote available for: %s' % symbol

def get_quotes(symbols):
    symbol_value_list = []
    for symbol in symbols:
        symbol_value_list.append(get_quote(symbol))
    return symbol_value_list
