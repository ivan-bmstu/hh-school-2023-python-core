from bisect import bisect_left, bisect_right
from my_logger import MyLogger


class Market:

    # структура класса Market с единым списком напитков выбрана исходя из функциональных требований
    @MyLogger.log_func_start_time_duration
    def __init__(self, wines: list = None, beers: list = None) -> None:
        # проиндексируем напитки по дате производства
        self.drinks = sorted(wines + beers, key=lambda x: x.production_date)
        # словарь по названию
        self.drinks_dict_by_title = {drink.title: drink for drink in sorted(self.drinks, key=lambda x: x.title)}

    @MyLogger.log_func_start_time_duration
    def has_drink_with_title(self, title=None) -> bool:
        if title in self.drinks_dict_by_title:
            return True
        else:
            return False

    @MyLogger.log_func_start_time_duration
    def get_drinks_sorted_by_title(self) -> list:
        return list(self.drinks_dict_by_title.values())

    @MyLogger.log_func_start_time_duration
    def get_drinks_by_production_date(self, from_date=None, to_date=None) -> list:
        if from_date > to_date:
            temp = from_date
            from_date = to_date
            to_date = temp
        if from_date > self.drinks[-1].production_date or to_date < self.drinks[0].production_date:
            return list()
        start = bisect_left(self.drinks, from_date, key=lambda x: x.production_date)
        end = bisect_right(self.drinks, to_date, key=lambda x: x.production_date)
        return list(self.drinks[start:end:])
