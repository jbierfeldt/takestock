#       Jackson Bierfeldt          #
from django.db import models


####### Stock Models #######


class Stock(models.Model):

#A stock whose current_price is updated every minute by a cronned script
#running on the server. The current_price updating script gets all Stock objects
#and runs Google Finance queries on each Stock

#Stock has no relation to a particular owner, for that, see StockInstance model below

    ticker = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __unicode__(self):
        return str(self.ticker + ">" + str(self.current_price))
        

class StockInstance(models.Model):

#A middle-man model which links a Stock model to an owner (see Club model below.)

#A single owner may possess multiple instances of a single stock purchased at different times
#ex. December 9, 2012 - Owner buys 20 shares of AAPL at $500
#    December 13, 2012 - Owner buys 15 shares of AAPL at $482

    owner = models.ForeignKey('Club')
    stock = models.ForeignKey(Stock)
    
    def current_price(self):
    #Current Price of relevant stock
        return self.stock.current_price
    
    shares = models.IntegerField()
    purchase_date = models.DateTimeField()
    purchase_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    #if is_open is False, the instance is considered a closed position
    is_open = models.BooleanField(default=True)
    sell_date = models.DateTimeField(blank=True, null=True)
    sell_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    def current_value(self):
        #Current value of this stock instance
        #ex. $200 Current Price * 10 shares = $2000 
        return (self.current_price() * self.shares)
        
    def purchase_value(self):
        #Purchase value of this stock instance
        #ex. $195 Purchase Price * 10 shares = $1950
        return (self.purchase_price * self.shares)    
        
    def percent_gl(self):
        #Percent Gained/Lost
        #ex. ($2000 Current Value - $1950 Purchase Value) / ($1950 Purchase Value) = .03 (03%) Gained
        return ((self.current_value() - self.purchase_value()) / (self.purchase_value()))
        
    def amount_gl(self):
        #Dollar Value Gained/Lost
        #ex. $2000 Current Value - $1950 Purchase Value = $50 Gained
        return (self.current_value() - self.purchase_value())
        
    def total_percentage(self):
        #Percent of Club Value (all club assets including cash) which this stock instance comprises
        #ex. $2000 Current Value / $10000 Club Total Assests = .20 (20%)
        return (self.current_value() / self.owner.current_value())
        
    def __unicode__(self):
        return str(str(self.shares) + str(" of ") + str(self.stock.ticker))
        
        
####### Member Models #######

    
class Member(models.Model):
#Members may belong to multiple clubs. The Member model has no relation to a club

#See MemberInstance model below
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=75, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
        

class MemberInstance(models.Model):

#A middle-man model which links a Member model to an owner (see Club model below.)

#A single member may belong to multiple clubs at the same time
#ex. John has 5 shares of "Sandstone Investment Club"
#    John has 15 shares of "Blackwell Investment Firm"
    
    owner = models.ForeignKey('Club')
    member = models.ForeignKey(Member)
    shares = models.DecimalField(max_digits=20, decimal_places=2)
    
    receive_daily_emails = models.BooleanField(default=False)
    receive_weekly_emails = models.BooleanField(default=False)
    receive_monthly_emails = models.BooleanField(default=False)
    receive_yearly_emails = models.BooleanField(default=False)
    
    def total_share_value(self):
    #Total Dollar value of all of particular member's shares of a club
    #ex. Sandstone Investment Club's Share Price is $20 and John has 5 shares
    #ex. cont. $20 * 5 shares = $100 value of John's shares in Sandstone Investment Club
        return (self.shares * self.owner.current_price())
        
    def total_share_percentage(self):
    #Percent of a club that a particular member owns
    #ex. John has $100 of Sandstone Investment, Sandstone Investment is worth $1000
    #ex. cont. $100 / $1000 = .10 (10%) John owns 10% of Sandstone Investment's Value
        return (float(self.total_share_value()) / float(self.owner.current_value()))
        
        
####### Club Models #######

    
class Club(models.Model):
###A Stock Club

#A club has members (MemberInstance) and buys Stocks (StockInstance).

#A note on the real-life purpose of stock clubs: Small-tim individual investors often do not have the 
#buying power to make powerful stock purchases. A single individual may not be able to buy 50 shares
#of a stock priced at $500 each. This individual joins a stock club, possibly with friends, family, or co-workers.
#The stock club has a number of shares that each member owns some of. The stock CLUB may own shares of many different
#STOCKS, but the club only has ONE stock price--its own.

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cash = models.DecimalField(max_digits=20, decimal_places=2)

    def total_shares(self):
    #The number of shares of the club that exist
    #ex. John has 6 shares of the club; Bob has 4 shares of the club
    #ex. cont. The club has (6+4=9) 10 total shares among its members.
        shares = 0
        for member in self.memberinstance_set.select_related():
            shares = shares + member.shares
        return shares
    
    def current_value(self):
    #The current value of the club
    #The current value of each stock instance plus the club's uninvested cash
    #ex. $200 from AAPL StockInstance + $400 from GOOG Instance + $20 cash = $620
        value = 0
        for stock in self.stockinstance_set.select_related():
            if stock.is_open == True:
                value = value + stock.current_value()
            else:
                pass
        return (self.cash + value)

    def current_price(self):
    #The club's current share price
    #The current value of the club divided by the total number of shares of the club
    #ex. $620 Club Current Value / 10 Total Shares = $62 per share
        return (self.current_value() / self.total_shares())
        
    def cash_total_percentage(self):
    #Percent of club's current value that is uninvested cash
        return ((self.cash) / (self.current_value()))
                
    def __unicode__(self):
        return self.name
        
        
    
    
    
    
