import datetime as dt


class Calculator:
    """
    Class Calculator is a parent class.
    It receives limit and can add records,
    provides week stats and today stats
    """

    DAYS_IN_WEEK = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Receives object of class Record and adds a record"""
        self.records.append(record)

    def get_week_stats(self):
        """Calculates stats for past 7 days"""
        today = dt.date.today()
        return sum(self.records.amount for self.records in self.records
                   if (self.records.date - self.DAYS_IN_WEEK) < self
                   .records.date <= today)

    def get_today_stats(self):
        """Calculates stats for current day"""
        today = dt.date.today()
        return sum(self.records.amount for self.records in self.records
                   if self.records.date == today)


class Record:
    """
    Class Record receives data and saves it.
    Input - amount, comment, date
    """
    # Here we define input date format as DMY
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class CashCalculator(Calculator):
    """
    Class CashCalculator contains method get_today_cash_remained
    Limit is taken from parent class Calculator.
    Converts to RUB, EUR, USD
    """
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {
        'rub': ('руб', 1),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE)
    }

    CURRENCY_UNKNOWN = 'Валюта неизвестна'

    CASH_OVER_LIMIT = ('Денег нет, держись: твой долг - '
                       '{cash_debt_format} {currency_name}')
    CASH_UNDER_LIMIT = ('На сегодня осталось '
                        '{cash_remained_format} {currency_name}')
    CASH_LIMIT_REACHED = 'Денег нет, держись'

    def get_today_cash_remained(self, currency):
        """
        Calculates remaining cash for today.
        Receives currency and converts to it
        """

        if currency not in self.CURRENCIES:
            return self.CURRENCY_UNKNOWN
        today_cash_remained = round((self.limit - self.get_today_stats()
                                     ) / self.CURRENCIES[currency][1], 2)
        if today_cash_remained == 0:
            return self.CASH_LIMIT_REACHED
        if today_cash_remained > 0:
            return self.CASH_UNDER_LIMIT.format(
                cash_remained_format=today_cash_remained,
                currency_name=self.CURRENCIES[currency][0])
        else:
            return self.CASH_OVER_LIMIT.format(
                cash_debt_format=abs(today_cash_remained),
                currency_name=self.CURRENCIES[currency][0])


class CaloriesCalculator(Calculator):
    """
    Class CaloriesCalculator contains method get_calories_remained
    Limit is taken from parent class Calculator.
    """

    CALORIES_OVER_LIMIT = 'Хватит есть!'
    CALORIES_UNDER_LIMIT = ('Сегодня можно съесть что-нибудь ещё, '
                            'но с общей калорийностью '
                            'не более {calories_remained_format} кКал')

    def get_calories_remained(self):
        """Calculcates remained calories for today"""
        calories_remained = (self.limit - self.get_today_stats())
        if calories_remained > 0:
            return self.CALORIES_UNDER_LIMIT.format(
                calories_remained_format=calories_remained)
        else:
            return self.CALORIES_UNDER_LIMIT
