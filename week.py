import datetime

def switch_variable_weekly(current_value):

    current_date = datetime.datetime.now()


    day_of_week = current_date.weekday()


    is_even_week = (current_date.isocalendar()[1] % 2 == 0)

    if (is_even_week and day_of_week == 0) or (not is_even_week and day_of_week == 6):
        return 1 - current_value
    else:
        return current_value

current_value = 0
qw = switch_variable_weekly(current_value)
print(qw)