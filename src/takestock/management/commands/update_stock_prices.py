from django.core.management.base import BaseCommand, CommandError

from takestock.models import Stock
from takestock.stock_getter import get_quotes

class Command(BaseCommand):
    help = 'Gathers current stock prices from Google Finance using stock_getter script (imported) and updates all stocks in the database to reflect the current stock price.'
    
    def get_stock_dict(self):
        all_stocks = Stock.objects.all()
        stock_names = []
        
        for single_stock in all_stocks:
            stock_names.append(str(single_stock.ticker))
        
        stock_values = get_quotes(stock_names)
        stock_dict = dict(zip(stock_names, stock_values))
        
        return stock_dict
    
    def handle(self, *args, **options):
    
        stock_dict = self.get_stock_dict()
        print stock_dict
        for ticker, value in stock_dict.items():
            Stock.objects.filter(ticker=ticker).update(current_price=value)
            
    
    
