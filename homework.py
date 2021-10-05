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
        self.records.append(record)

    def get_week_stats(self):
        """Calculates stats for past 7 days"""
        today = dt.date.today()
        week = today - self.DAYS_IN_WEEK
        return sum(record.amount for record in self.records
                   if (week < record.date <= today))

    def get_today_stats(self):
        """Calculates stats for current day"""
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)


class Record:
    """
    Class Record receives data and saves it.
    Input - amount, comment, date
    """
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
    """
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {
        'rub': ('руб', 1),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE)
    }

    CURRENCY_UNKNOWN = 'Значение {name} недопустимо'
    OVER_LIMIT = ('Денег нет, держись: твой долг - {cash_debt} {name}')
    UNDER_LIMIT = ('На сегодня осталось {cash_remained} {name}')
    LIMIT_REACHED = 'Денег нет, держись'

    def get_today_cash_remained(self, currency):
        """
        Calculates remaining cash for today.
        Receives currency and converts to it
        """
        if currency not in self.CURRENCIES:
            raise ValueError(self.CURRENCY_UNKNOWN.format(name=currency))
        today_cash_remained = self.limit - self.get_today_stats()
        name, rate = self.CURRENCIES[currency]
        if today_cash_remained == 0:
            return self.LIMIT_REACHED
        today_cash_remained = round(today_cash_remained / rate, 2)
        if today_cash_remained > 0:
            return self.UNDER_LIMIT.format(
                cash_remained=today_cash_remained,
                name=name)
        return self.OVER_LIMIT.format(
            cash_debt=abs(today_cash_remained),
            name=name)


class CaloriesCalculator(Calculator):
    """
    Class CaloriesCalculator contains method get_calories_remained
    Limit is taken from parent class Calculator.
    """

    OVER = 'Хватит есть!'
    UNDER = ('Сегодня можно съесть что-нибудь ещё, '
             'но с общей калорийностью '
             'не более {calories} кКал')

    def get_calories_remained(self):
        """Calculcates remained calories for today"""
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return self.UNDER.format(calories=calories_remained)
        return self.OVER
