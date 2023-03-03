from datetime import datetime
from math import exp, log, sqrt

import pytest

import src.equations as eq
import src.source as source


@pytest.fixture
def example_source():
    example = source.Cf()
    return example


def test_source_representation(example_source):
    expected = 'src.source.Cf()'
    actual = example_source.__repr__()
    assert actual == expected, f'Source representation should be {expected}, not {actual}.'


def test_source_string(example_source):
    expected = '252-Cf source'
    actual = str(example_source)
    assert actual == expected, f'Source string should be {expected}, not {actual}.'


def test_source_calibration_date(example_source):
    expected = '2012/05/20'
    actual = example_source.calibration_date
    assert actual == expected, f'Source calibration date should be {expected}, not {actual}.'


def test_source_calibration_strength(example_source):
    expected = (5.471E+08, 5.471E+08 * 1.3 / 100, 1.3)
    actual = example_source.calibration_strength
    assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'


def test_source_half_life(example_source):
    expected = (2.6470, 0.0026, 0.0026 / 2.6470 * 100)
    actual = example_source.half_life
    assert actual == expected, f'Source half life should be {expected}, not {actual}.'


def test_source_anisotropy_factor(example_source):
    expected = (1.051, 0.019, 0.019 / 1.051 * 100)
    actual = example_source.anisotropy_factor
    assert actual == expected, f'Source anisotropy factor should be {expected}, not {actual}.'


def test_source_linear_attenuation_coefficient(example_source):
    expected = (1055e-7, 1055e-7 * 1.5 / 100, 1.5)
    actual = example_source.linear_attenuation_coefficient
    assert actual == expected, f'Source linear attenuation coefficient should be {expected}, not {actual}.'


def test_source_fluence_to_dose_conversion_factor(example_source):
    expected = (385, 385 * 1 / 100, 1)
    actual = example_source.fluence_to_dose_conversion_factor
    assert actual == expected, f'Source fluence-to-dose conversion factor should be {expected}, not {actual}.'


def test_source_neutron_effectiveness(example_source):
    expected = (0.5, 0.1, 0.1 / 0.5 * 100)
    actual = example_source.neutron_effectiveness
    assert actual == expected, f'Source neutron effectiveness should be {expected}, not {actual}.'


def test_source_total_air_scatter_component(example_source):
    expected = (0.00012, 0.00012 * 15 / 100, 15)
    actual = example_source.total_air_scatter_component
    assert actual == expected, f'Source total air scatter component should be {expected}, not {actual}.'


def test_decay_time(example_source):
    initial_date = example_source.calibration_date
    final_date = '2013/05/20'
    expected = eq.elapsed_time(initial_date, final_date)
    actual = example_source.decay_time('2013/05/20')
    assert actual == expected, f'Source decay time should be {expected}, not {actual}.'


def test_decay_factor(example_source):
    # TODO: test fails
    # Data
    initial_date, final_date = '2012/01/01', '2012/12/31'
    t12, u_t12, ur_t12 = example_source.half_life
    # Elapsed time
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    t = final_date - initial_date
    t = t.days
    u_t = eq.u_t_days
    ur_t = u_t / t * 100
    # Unit conversion
    t12 = t12 * 365.242
    # Decay factor
    f = exp(-log(2) * t / t12)
    ur_f = sqrt((log(2) * t / t / 12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))
    u_f = f * ur_f / 100
    expected = (f, u_f, ur_f)
    # Actual value
    actual = example_source.decay_factor('2012/01/01', '2012/12/31')
    assert actual == expected, f'Source decay factor should be {expected}, not {actual}.'
