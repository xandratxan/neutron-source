from datetime import datetime
from math import exp, log, sqrt

import src.equations as eq


def test_elapsed_time():
    initial_date, final_date = '2012/01/01', '2012/12/31'
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    t = final_date - initial_date
    t = t.days
    u_t = eq.u_t_days
    ur_t = u_t / t * 100
    expected = t, u_t, ur_t
    actual = eq.elapsed_time(initial_date='2012/01/01', final_date='2012/12/31')
    assert actual == expected, f'Elapsed time should be {expected}, not {actual}.'


def test_percentage_uncertainty():
    m, u_m = 100, 10
    expected = u_m / m * 100
    actual = eq.percentage_uncertainty(m=100, u_m=10)
    assert actual == expected, f'Percentage uncertainty should be {expected}, not {actual}.'


def test_absolute_uncertainty():
    m, ur_m = 100, 10
    expected = m * ur_m / 100
    actual = eq.absolute_uncertainty(m=100, ur_m=10)
    assert actual == expected, f'Absolute uncertainty should be {expected}, not {actual}.'


def test_decay_factor_value():
    t, t12 = 1, 300
    expected = exp(-log(2) * t / t12)
    actual = eq.decay_factor_value(t=1, t12=300)
    assert actual == expected, f'Source decay factor value should be {expected}, not {actual}.'


def test_decay_factor_uncertainty():
    t, t12, ur_t, ur_t12 = 1, 300, 10, 1
    expected = sqrt((log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
    actual = eq.decay_factor_uncertainty(t=1, t12=300, ur_t=10, ur_t12=1)
    assert actual == expected, f'Source decay factor relative uncertainty should be {expected}, not {actual}.'


def test_strength_value():
    b0, t, t12 = 10 ** 8, 1, 300
    expected = b0 * exp(-log(2) * t / t12)
    actual = eq.strength_value(b0=10 ** 8, t=1, t12=300)
    assert actual == expected, f'Source strength value should be {expected}, not {actual}.'


def test_strength_relative_uncertainty():
    t, t12, ur_b0, ur_t, ur_t12 = 1, 300, 5, 10, 1
    expected = sqrt(ur_b0 ** 2 + (log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
    actual = eq.strength_relative_uncertainty(t=1, t12=300, ur_b0=5, ur_t=10, ur_t12=1)
    assert actual == expected, f'Source strength relative uncertainty should be {expected}, not {actual}.'
