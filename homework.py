
import datetime as dt

DATE_PATTERN = '%d.%m.%Y'


class Calculator:
    """Материнский класс калькулятора денег и каллорий."""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Транслируем запрос во внешний класс для обработки данных."""
        self.records.append(record)

    def get_today_stats(self):
        """Подсчёт данных за день."""
        now_date = dt.date.today()
        return sum(days.amount for days in self.records
                   if days.date == now_date)

    def get_week_stats(self):
        """Подсчёт данных за неделю."""
        now_date = dt.date.today()
        old_date = now_date - dt.timedelta(days=7)
        return sum(days.amount for days in self.records
                   if old_date < days.date <= now_date)

    def get_difference(self):
        """Вычисление разницы между заданным лимитом и состоянием на
        текущий момент.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Класс калькулятора каллорий."""
    REMAINED_CALORIES = ('Сегодня можно съесть что-нибудь ещё, но с общей '
                         'калорийностью не более {calories} кКал')
    LIMIT = 'Хватит есть!'

    def get_calories_remained(self):
        """Остаток каллорий"""
        calories = self.get_difference()
        if calories <= 0:
            return 'Хватит есть!'
        return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {calories} кКал')


class CashCalculator(Calculator):
    """Класс калькулятора расходов."""
    USD_RATE = 72.88
    EURO_RATE = 85.47
    RUB_RATE = 1

    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
    }

    def get_today_cash_remained(self, currency: str):
        """Функция отчёта о состоянии дневного баланса с конвертацией в
        необходимую валюту.
        """
        if currency not in self.CURRENCIES:
            raise ValueError(f'Ошибка: Валюта "{currency}" не '
                             'поддерживается')
        cash = self.get_difference()
        if cash == 0:
            return 'Денег нет, держись'
        cur_name, cur_money = self.CURRENCIES[currency]
        cash = round(cash / cur_money, 2)
        if cash > 0:
            return (f'На сегодня осталось {cash} {cur_name}')
        cash = abs(cash)
        return (f'Денег нет, держись: твой долг - {cash} {cur_name}')


class Record:
    """Обработка данных, возможно встраивание проверок на соответствие"""
    def __init__(self, amount, comment, date=None):
        self.amount = abs(amount)
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_PATTERN).date()


if __name__ == '__main__':
    pass
