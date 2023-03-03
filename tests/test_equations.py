from datetime import datetime
from math import exp, log, sqrt

import src.equations as eq


def test_elapsed_time():
    initial_date, final_date = '2012/01/01', '2012/12/31'
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    time = final_date - initial_date
    time = time.days
    uncertainty = eq.u_t_days
    percentage = eq.percentage_uncertainty(time, uncertainty)
    expected = time, uncertainty, percentage
    actual = eq.elapsed_time('2012/01/01', '2012/12/31')
    assert actual == expected, f'Elapsed time should be {expected}, not {actual}.'


def test_percentage_uncertainty():
    value, absolute_uncertainty = 100, 10
    expected = absolute_uncertainty / value * 100
    actual = eq.percentage_uncertainty(100, 10)
    assert actual == expected, f'Percentage uncertainty should be {expected}, not {actual}.'


def test_absolute_uncertainty():
    value, percentage_uncertainty = 100, 10
    expected = value * percentage_uncertainty / 100
    actual = eq.percentage_uncertainty(100, 10)
    assert actual == expected, f'Percentage uncertainty should be {expected}, not {actual}.'


def test_decay_factor_value():
    decay_time, half_life = 1, 300
    expected = exp(-log(2) * decay_time / half_life)
    actual = eq.decay_factor_value(1, 300)
    assert actual == expected, f'Source decay factor value should be {expected}, not {actual}.'


def test_decay_factor_uncertainty():
    decay_time, half_life = 1, 300
    decay_time_relative_uncertainty, half_life_relative_uncertainty = 10, 1
    square_sum = decay_time_relative_uncertainty ** 2 + half_life_relative_uncertainty ** 2
    multiplication_factor = (log(2) * decay_time / half_life) ** 2
    expected = sqrt(multiplication_factor * square_sum)
    actual = eq.decay_factor_uncertainty(1, 300, 10, 1)
    assert actual == expected, f'Source decay factor relative uncertainty should be {expected}, not {actual}.'
