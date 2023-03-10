import pytest

import src.source.source as source


@pytest.fixture
def example_source():
    example = source.Cf()
    return example


class TestSourceDefinition:
    def test_source_representation(self, example_source):
        expected = 'src.source.source.Cf()'
        actual = example_source.__repr__()
        assert actual == expected, f'Source representation should be {expected}, not {actual}.'

    def test_source_string(self, example_source):
        expected = '252-Cf radionuclide neutron source'
        actual = str(example_source)
        assert actual == expected, f'Source string should be {expected}, not {actual}.'

    def test_source_calibration_date(self, example_source):
        expected = '2012/05/20'
        actual = example_source.calibration_date
        assert actual == expected, f'Source calibration date should be {expected}, not {actual}.'

    def test_source_calibration_strength(self, example_source):
        expected = (5.471E+08, 5.471E+08 * 1.3 / 100, 1.3)
        actual = example_source.calibration_strength
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_source_half_life(self, example_source):
        expected = (2.6470, 0.0026, 0.0026 / 2.6470 * 100)
        actual = example_source.half_life
        assert actual == expected, f'Source half life should be {expected}, not {actual}.'

    def test_source_anisotropy_factor(self, example_source):
        expected = (1.051, 0.019, 0.019 / 1.051 * 100)
        actual = example_source.anisotropy_factor
        assert actual == expected, f'Source anisotropy factor should be {expected}, not {actual}.'

    def test_source_linear_attenuation_coefficient(self, example_source):
        expected = (1055e-7, 1055e-7 * 1.5 / 100, 1.5)
        actual = example_source.linear_attenuation_coefficient
        assert actual == expected, f'Source linear attenuation coefficient should be {expected}, not {actual}.'

    def test_source_fluence_to_dose_conversion_factor(self, example_source):
        expected = (385, 385 * 1 / 100, 1)
        actual = example_source.fluence_to_dose_conversion_factor
        assert actual == expected, f'Source fluence-to-dose conversion factor should be {expected}, not {actual}.'

    def test_source_neutron_effectiveness(self, example_source):
        expected = (0.5, 0.1, 0.1 / 0.5 * 100)
        actual = example_source.neutron_effectiveness
        assert actual == expected, f'Source neutron effectiveness should be {expected}, not {actual}.'

    def test_source_total_air_scatter_component(self, example_source):
        expected = (0.00012, 0.00012 * 15 / 100, 15)
        actual = example_source.total_air_scatter_component
        assert actual == expected, f'Source total air scatter component should be {expected}, not {actual}.'


class TestSourceMethods:
    def test_decay_time(self, example_source):
        expected = (2922, 1, 0.034223134839151265)
        actual = example_source.decay_time(date='2020/05/20')
        assert actual == expected, f'Source decay time should be {expected}, not {actual}.'

    def test_decay_factor_one_date(self, example_source):
        expected = (0.12307796649188105, 0.0002681946089174612, 0.21790627239129184)
        actual = example_source.decay_factor(final_date='2020/05/20')
        assert actual == expected, f'Source decay factor should be {expected}, not {actual}.'

    def test_decay_factor_two_dates(self, example_source):
        expected = (0.12307796649188105, 0.0002681946089174612, 0.21790627239129184)
        actual = example_source.decay_factor(final_date='2020/05/20', initial_date='2012/05/20')
        assert actual == expected, f'Source decay factor should be {expected}, not {actual}.'

    def test_source_strength(self, example_source):
        expected = (67335955.46770813, 887579.630636847, 1.3181362386140016)
        actual = example_source.strength(date='2020/05/20')
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

    def test_source_strength_at_calibration_date(self, example_source):
        expected = example_source.calibration_strength
        actual = example_source.strength(date='2012/05/20')
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

#     def test_fluence_rate(self):
#         expected = None
#         actual = example_source.fluence_rate(date=None, distance=None)
#         assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'
#
#     def test_ambient_dose_equivalent_rate(self):
#         expected = None
#         actual = example_source.ambient_dose_equivalent_rate(date=None, distance=None)
#         assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'
