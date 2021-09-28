import datetime as dt


class Calculator:
    """
    Class Calculator is a parent class.
    It receives limit and can add records,
    provides week stats and today stats
    """

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()

    def add_record(self, Record):
        """Receives object of class Record and adds record"""
        self.records.append(Record)

    def get_week_stats(self):
        """Calculates stats for past 7 days"""
        week_stats = 0
        for record in self.records:
            if (
                dt.datetime.now().date() - dt.timedelta(days=7)
                 ) < record.date <= dt.datetime.now().date():
                week_stats += record.amount
        return (week_stats)

    def get_today_stats(self):
        """Calculates stats for current day"""
        today_stats = 0
        for i in range(len(self.records)):
            if self.records[i].date == self.today:
                today_stats += self.records[i].amount
        return(today_stats)


class Record:
    """
    Class Record receives data and saves it.
    Input - amount, comment, date
    """

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        # date equals current date if not provided
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    """
    Class CashCalculator contains method get_today_cash_remained
    Limit is taken from parent class Calculator.
    Converts to RUB, EUR, USD
    """

    def __init__(self, limit):
        super().__init__(limit)

        self.USD_RATE = 72.72
        self.EURO_RATE = 85.23

    def get_today_cash_remained(self, currency):
        """Calculates remaining cash for today.
        Receives currency and converts to it
        """
        self.currency = currency
        self.today_cash_remained = (self.limit - CashCalculator
                                    .get_today_stats(self))

        if self.currency == 'usd':
            self.today_cash_remained = (self.today_cash_remained / self
                                        .USD_RATE)
            self.currency = 'USD'
        if self.currency == 'eur':
            self.today_cash_remained = (self.today_cash_remained / self
                                        .EURO_RATE)
            self.currency = 'Euro'
        if self.currency == 'rub':
            self.currency = 'руб'

        self.today_cash_remained = round(self.today_cash_remained, 2)

        if self.today_cash_remained > 0:
            self.output = ('На сегодня осталось '
                           f'{self.today_cash_remained} {self.currency}')
        elif self.today_cash_remained < 0:
            self.today_cash_remained = (-1) * self.today_cash_remained
            self.output = ('Денег нет, держись: твой долг - '
                           f'{self.today_cash_remained} {self.currency}')
        else:
            self.output = 'Денег нет, держись'

        return self.output


class CaloriesCalculator(Calculator):
    """
    Class CaloriesCalculator contains method get_calories_remained
    Limit is taken from parent class Calculator.
    """

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """Calculcates remained calories and output the message"""

        self.calories_remained = (self.limit - CaloriesCalculator
                                  .get_today_stats(self))

        if self.calories_remained > 0:
            self.output = ('Сегодня можно съесть что-нибудь ещё, '
                           'но с общей калорийностью '
                           f'не более {self.calories_remained} кКал')
        else:
            self.output = 'Хватит есть!'

        return self.output
