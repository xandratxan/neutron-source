import pytest
from src.source import Cf


@pytest.fixture
def example_source():
    source = Cf()
    return source


def test_source_representation(example_source):
    expected = 'src.source.Cf()'
    actual = example_source.__repr__()
    assert actual == expected, f'Source representation should be {expected}.'


def test_source_string(example_source):
    expected = '252-Cf source'
    actual = str(example_source)
    assert actual == expected, f'Source string should be {expected}.'


def test_source_calibration_date(example_source):
    expected = '2012/05/20'
    actual = example_source.calibration_date
    assert actual == expected, f'Source calibration date should be {expected}.'


def test_source_calibration_strength(example_source):
    expected = (5.471E+08, 5.471E+08 * 1.3 / 100, 1.3)
    actual = example_source.calibration_strength
    assert actual == expected, f'Source calibration strength should be {expected}.'


def test_source_half_life(example_source):
    expected = (2.6470, 0.0026, 0.0026 / 2.6470 * 100)
    actual = example_source.half_life
    assert actual == expected, f'Source half life should be {expected}.'


def test_source_anisotropy_factor(example_source):
    expected = (1.051, 0.019, 0.019 / 1.051 * 100)  # DT-LMRI-2201
    actual = example_source.anisotropy_factor
    assert actual == expected, f'Source anisotropy factor should be {expected}.'


def test_source_linear_attenuation_coefficient(example_source):
    expected = (1055e-7, 1055e-7 * 1.5 / 100, 1.5)
    actual = example_source.linear_attenuation_coefficient
    assert actual == expected, f'Source linear attenuation coefficient should be {expected}.'


def test_source_fluence_to_dose_conversion_factor(example_source):
    expected = (385, 385 * 1 / 100, 1)
    actual = example_source.fluence_to_dose_conversion_factor
    assert actual == expected, f'Source fluence-to-dose conversion factor should be {expected}.'


def test_source_neutron_effectiveness(example_source):
    expected = (0.5, 0.1, 0.1 / 0.5 * 100)
    actual = example_source.neutron_effectiveness
    assert actual == expected, f'Source neutron effectiveness should be {expected}.'


def test_source_total_air_scatter_component(example_source):
    expected = (0.00012, 0.00012 * 15 / 100, 15)
    actual = example_source.total_air_scatter_component
    assert actual == expected, f'Source total air scatter component should be {expected}.'
