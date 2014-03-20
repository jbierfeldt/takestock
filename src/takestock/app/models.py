from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    """
    Represents a single stock.

    current_price is updated every minute by a cron script running on the
    server. The current_price updating script gets all Stock objects and runs
    Google Finance queries on each Stock.

    A stock has no relation to a particular owner. For that, see
    the StockInstance model below.
    """
    ticker = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __unicode__(self):
        return str(self.ticker + ">" + str(self.current_price))


class StockInstance(models.Model):
    """
    Links a Stock to a Club.

    A single owner may possess multiple instances of a single stock purchased
    at different times

    Example:

        December 9, 2012 - Owner buys 20 shares of AAPL at $500
        December 13, 2012 - Owner buys 15 shares of AAPL at $482

    """
    owner = models.ForeignKey('Club')
    stock = models.ForeignKey(Stock)

    def current_price(self):
        """Current price of related stock."""
        return self.stock.current_price

    shares = models.IntegerField()
    purchase_date = models.DateTimeField()
    purchase_price = models.DecimalField(max_digits=20, decimal_places=2)

    #if is_open is False, the instance is considered a closed position
    is_open = models.BooleanField(default=True)
    sell_date = models.DateTimeField(blank=True, null=True)
    sell_price = models.DecimalField(max_digits=20, decimal_places=2,
                                     blank=True, null=True)

    def current_value(self):
        """
        Current value of this stock instance.

        Example: $200 current price * 10 shares = $2000
        """
        return (self.current_price() * self.shares)

    def purchase_value(self):
        """
        Purchase value of this stock instance.

        Example: $195 purchase price * 10 shares = $1950
        """
        return (self.purchase_price * self.shares)

    def percent_gl(self):
        """
        Percent gained/lost.

        Example:

            Assume current_value is $2000, purchase_value is $1950.
            Returns ($2000 - $1950) / $1950 = .03 (3%)

        """
        return ((self.current_value() - self.purchase_value())
                / (self.purchase_value()))

    def amount_gl(self):
        """
        Dollar value gained/lost.

        Example: $2000 current value - $1950 purchase value = $50
        """
        return (self.current_value() - self.purchase_value())

    def total_percentage(self):
        """
        Percentage of club value this stock instance represents.

        Club value is the sum of all assets including cash.

        Example: $2000 current value / $10000 total assets = .20 (20%)
        """
        return (self.current_value() / self.owner.current_value())

    def __unicode__(self):
        return str(str(self.shares) + str(" of ") + str(self.stock.ticker))


class MemberInstance(models.Model):
    """
    Links a Member to a Club.

    A single member may belong to multiple clubs at the same time

    Example:

        John has 5 shares of "Sandstone Investment Club"
        John has 15 shares of "Blackwell Investment Firm"

    """
    owner = models.ForeignKey('Club')
    member = models.ForeignKey(User)
    shares = models.DecimalField(max_digits=20, decimal_places=2)
    receive_daily_emails = models.BooleanField(default=False)
    receive_weekly_emails = models.BooleanField(default=False)
    receive_monthly_emails = models.BooleanField(default=False)
    receive_yearly_emails = models.BooleanField(default=False)

    def total_share_value(self):
        """
        Total dollar value of shares in the related club.

        Example:

            Assume John owns 5 shares of Sandstone Investment Club, whose
            share price is $20.
            Returns $20 * 5 = $100

        """
        return (self.shares * self.owner.current_price())

    def total_share_percentage(self):
        """
        Percent of a club the related member owns.

        Example:

            Assume John owns $100 of Sandstone Investment, which is
            worth $1000.
            Returns $100 / $1000 = .10 (10%) of the total club value
        """
        return (float(self.total_share_value())
                / float(self.owner.current_value()))


class Club(models.Model):
    """
    Represents a stock club.

    A club has members (MemberInstance) and buys Stocks (StockInstance).

    A note on the real-life purpose of stock clubs: Small-time individual
    investors often do not have the buying power to make powerful stock
    purchases. A single individual may not be able to buy 50 shares of a stock
    priced at $500 each. This individual joins a stock club, possibly with
    friends, family, or co-workers. The stock club has a number of shares that
    each member owns some of. The stock CLUB may own shares of many different
    STOCKS, but the club only has ONE stock price -- its own.
    """
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cash = models.DecimalField(max_digits=20, decimal_places=2)

    def total_shares(self):
        """
        Total number of shares in this club.

        Example: John has 6 shares, Bob has 4; there are 6 + 4 = 10 total
        shares.
        """
        shares = 0
        for member in self.memberinstance_set.select_related():
            shares = shares + member.shares
        return shares

    def current_value(self):
        """
        Current value of the club.

        The current value is the sum of the current value of each stock
        instance plus the club's uninvested cash.

        Example:

            Sandstone Investment owns $200 of AAPL and $400 of GOOG, with
            $20 in idle cash.
            Returns $200 + $400 + $20 = $620

        """
        value = 0
        for stock in self.stockinstance_set.select_related():
            if stock.is_open:
                value = value + stock.current_value()
            else:
                pass
        return (self.cash + value)

    def current_price(self):
        """
        Current share price of the club.

        Current share price is calculated by dividing the current value of
        the club by the number of shares.

        Example:

            Sandstone Investment has a current value of $620, and
            10 total shares.
            Returns $620 / 10 = $62

        """
        return (self.current_value() / self.total_shares())

    def cash_total_percentage(self):
        """Percent of current value in idle cash."""
        return ((self.cash) / (self.current_value()))

    def __unicode__(self):
        return self.name
