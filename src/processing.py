def filter_by_state(dict_for_state: list[dict] , state : str ="EXECUTED") -> list[dict]:
    """Принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED' ). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению."""
    filtered_list  = []
    for d in dict_for_state:
        if d.get('state') == state:
            filtered_list.append(d)
    return filtered_list


def sort_by_date(dict_sort_by_date: list[dict], reverse: bool=True) -> list[dict]:
    """ Gринимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание), взвращает новый список, отсортированный по дате (date)"""
    return sorted(dict_sort_by_date, key= lambda x: x.get('date'), reverse=reverse)





