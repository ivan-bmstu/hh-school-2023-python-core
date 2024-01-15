from bisect import bisect_left, bisect_right

from drink import Drink
from my_logger import MyLogger


class Market:

    # структура класса Market с единым списком напитков выбрана исходя из функциональных требований
    @MyLogger.log_func_start_time_duration
    def __init__(self, wines: list = None, beers: list = None) -> None:
        # проиндексируем список валидных напитков по дате производства и словарь по названию
        # напитки без наименования нас не интересуют
        temp_drinks = [x for x in (wines + beers) if (isinstance(x, Drink) and x.title is not None)]
        # словарь по названию; здесь есть напитки с датой производства None
        self.drinks_dict_by_title = {drink.title: drink for drink in sorted(temp_drinks, key=lambda x: x.title)}
        # отсортированные напитки по дате производства (без None даты производства)
        self.drinks = sorted([x for x in temp_drinks if x.production_date is not None], key=lambda x: x.production_date)

    @MyLogger.log_func_start_time_duration
    def has_drink_with_title(self, title=None) -> bool:
        return title in self.drinks_dict_by_title

    @MyLogger.log_func_start_time_duration
    def get_drinks_sorted_by_title(self) -> list:
        return sorted(list(self.drinks_dict_by_title.values()), key=lambda x: x.title)

    # функция возвращает напитки произведенные в определенный (или неопределенный) промежуток времени
    @MyLogger.log_func_start_time_duration
    def get_drinks_by_production_date(self, from_date=None, to_date=None) -> list:
        # иначе может быть IndexError
        if not self.drinks:
            if from_date is None or to_date is None:
                return self.get_drinks_without_production_date()
            else:
                return list()

        if from_date is None and to_date is None:
            return self.drinks + self.get_drinks_without_production_date()

        if from_date is None and to_date is not None:
            if to_date < self.drinks[0].production_date:
                return self.get_drinks_without_production_date()
            else:
                end = bisect_right(self.drinks, to_date, key=lambda x: x.production_date)
                return self.get_drinks_without_production_date() + list(self.drinks[0:end:])

        if from_date is not None and to_date is None:
            if from_date > self.drinks[-1].production_date:
                return self.get_drinks_without_production_date()
            else:
                start = bisect_left(self.drinks, from_date, key=lambda x: x.production_date)
                return list(self.drinks[start:-1:]) + self.get_drinks_without_production_date()

        if from_date > to_date:
            temp = from_date
            from_date = to_date
            to_date = temp
        if from_date > self.drinks[-1].production_date or to_date < self.drinks[0].production_date:
            return list()
        start = bisect_left(self.drinks, from_date, key=lambda x: x.production_date)
        end = bisect_right(self.drinks, to_date, key=lambda x: x.production_date)
        return list(self.drinks[start:end:])

    # функция возвращает напитки, у которых нет даты производства
    @MyLogger.log_func_start_time_duration
    def get_drinks_without_production_date(self) -> list:
        return [x for x in self.drinks_dict_by_title.values() if x.production_date is None]
