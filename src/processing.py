from traceback import print_tb


def filter_by_state(*dict_for_state, state="EXECUTED"):
    filtered_list  = []
    for d in dict_for_state:
        if d.get('state') == state:
            filtered_list.append(d)
    return filtered_list
#return [item for item in dict_for_state if item.get('state') == state]


def sort_by_date(*dict_sort_by_date, reverse=True):
        sorted_date = sorted(dict_sort_by_date, key='date', reverse=True)



print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))
print(filter_by_state({'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}))




