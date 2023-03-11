import src.source.equations as eq
from src.source.source import years_to_days


def test_elapsed_time():
    expected = 2922
    actual = eq.elapsed_time(initial_date='2012/05/20', final_date='2020/05/20')
    assert actual == expected, f'Elapsed time should be {expected}, not {actual}.'


def test_decay_factor_value():
    expected = 0.12307796649188105
    actual = eq.decay_factor_value(t=2922, t12=2.6470 * years_to_days)
    assert actual == expected, f'Source decay factor value should be {expected}, not {actual}.'


def test_decay_factor_uncertainty():
    expected = 0.0021790627239129182
    actual = eq.decay_factor_uncertainty(t=2922, t12=2.6470 * years_to_days, ur_t=1 / 2922, ur_t12=0.0026 / 2.6470)
    assert actual == expected, f'Source decay factor relative uncertainty should be {expected}, not {actual}.'
