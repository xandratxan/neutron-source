import pytest
from magnitude import Magnitude

import src.source.source as source


# TODO: validate numbers
@pytest.fixture
def example_source():
    example = source.Cf()
    return example


class TestSourceDefinition:  # TODO rename to TestSourceAttributesValue
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
        expected = f'547100000.0 ± {5.471E+08 * 1.3 / 100} 1/s (1.3%)'
        actual = str(example_source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_source_half_life(self, example_source):
        expected = f'2.647 ± 0.0026 y ({0.0026 / 2.6470 * 100}%)'
        actual = str(example_source.half_life)
        assert actual == expected, f'Source half life should be {expected}, not {actual}.'

    def test_source_anisotropy_factor(self, example_source):
        expected = f'1.051 ± 0.019 ND ({0.019 / 1.051 * 100}%)'
        actual = str(example_source.anisotropy_factor)
        assert actual == expected, f'Source anisotropy factor should be {expected}, not {actual}.'

    def test_source_linear_attenuation_coefficient(self, example_source):
        expected = f'0.0001055 ± {1055e-7 * 1.5 / 100} 1/cm (1.5%)'
        actual = str(example_source.linear_attenuation_coefficient)
        assert actual == expected, f'Source linear attenuation coefficient should be {expected}, not {actual}.'

    def test_source_fluence_to_dose_conversion_factor(self, example_source):
        expected = f'385 ± {385 * 1 / 100} pSv·cm² (1.0%)'
        actual = str(example_source.fluence_to_dose_conversion_factor)
        assert actual == expected, f'Source fluence-to-dose conversion factor should be {expected}, not {actual}.'

    def test_source_neutron_effectiveness(self, example_source):
        expected = f'0.5 ± 0.1 ND ({0.1 / 0.5 * 100}%)'
        actual = str(example_source.neutron_effectiveness)
        assert actual == expected, f'Source neutron effectiveness should be {expected}, not {actual}.'

    def test_source_total_air_scatter_component(self, example_source):
        expected = f'0.00012 ± {0.00012 * 15 / 100} 1/cm (15.0%)'
        actual = str(example_source.total_air_scatter_component)
        assert actual == expected, f'Source total air scatter component should be {expected}, not {actual}.'


class TestSourceAttributesConsistency:
    def test_all_values_positive(self, example_source):
        for attr, magnitude in example_source.numeric_attributes():
            assert magnitude.value >= 0, f'Source {attr} value must be positive.'

    def test_all_uncertainties_positive(self, example_source):
        for attr, magnitude in example_source.numeric_attributes():
            assert magnitude.uncertainty >= 0, f'Source {attr} value must be positive.'

    def test_all_relative_uncertainties_positive(self, example_source):
        for attr, magnitude in example_source.numeric_attributes():
            assert magnitude.uncertainty >= 0, f'Source {attr} value must be positive.'

    def test_all_units_standard(self, example_source):
        assert example_source.calibration_strength.unit == '1/s'
        assert example_source.half_life.unit == 'y'
        assert example_source.anisotropy_factor.unit == 'ND'
        assert example_source.linear_attenuation_coefficient.unit == '1/cm'
        assert example_source.fluence_to_dose_conversion_factor.unit == 'pSv·cm²'
        assert example_source.neutron_effectiveness.unit == 'ND'
        assert example_source.total_air_scatter_component.unit == '1/cm'


class TestSourceMethods:
    date = '2020/05/20'
    distance = Magnitude(value=100, unit='cm', uncertainty=1)

    def test_decay_time(self, example_source):
        expected = f'2922 ± 1 d ({1 / 2922 * 100}%)'
        actual = str(example_source.decay_time(date=self.date))
        assert actual == expected, f'Source decay time should be {expected}, not {actual}.'

    def test_decay_factor(self, example_source):
        expected = f'0.12307796649188105 ± 0.0002681946089174612 ND (0.21790627239129182%)'
        actual = str(example_source.decay_factor(date=self.date))
        assert actual == expected, f'Source decay factor should be {expected}, not {actual}.'

    def test_source_strength(self, example_source):
        expected = f'67335955.46770813 ± 887579.6306368469 1/s (1.3181362386140014%)'
        actual = str(example_source.strength(date=self.date))
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

    def test_source_strength_at_calibration_date(self, example_source):
        expected = example_source.calibration_strength
        actual = example_source.strength(date=example_source.calibration_date)
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

    def test_fluence_rate(self, example_source):
        expected = f'563.170475934353 ± 14.906082662095244 1/cm²s (2.6468153603692817%)'
        actual = str(example_source.fluence_rate(date=self.date, distance=self.distance))
        assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'

    def test_ambient_dose_equivalent_rate(self, example_source):
        expected = f'780.5542796450133 ± 22.085178231439247 uSv/h (2.8294224767409286%)'
        actual = str(example_source.ambient_dose_equivalent_rate(date=self.date, distance=self.distance))
        assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'

    def test_source_information(self, example_source):
        expected = (
            f'Name: 252-Cf\n'
            f'Calibration date: 2012/05/20\n'
            f'Magnitude: value ± uncertainty (percentage uncertainty)\n'
            f'Calibration strength: 547100000.0 ± {5.471E+08 * 1.3 / 100} 1/s (1.3%)\n'
            f'Half life: 2.647 ± 0.0026 y ({0.0026 / 2.6470 * 100}%)\n'
            f'Anisotropy factor: 1.051 ± 0.019 ND ({0.019 / 1.051 * 100}%)\n'
            f'Linear attenuation coefficient: 0.0001055 ± {1055e-7 * 1.5 / 100} 1/cm (1.5%)\n'
            f'Fluence to dose conversion factor: 385 ± {385 * 1 / 100} pSv·cm² (1.0%)\n'
            f'Neutron effectiveness: 0.5 ± 0.1 ND ({0.1 / 0.5 * 100}%)\n'
            f'Total air scatter component: 0.00012 ± {0.00012 * 15 / 100} 1/cm (15.0%)'
        )
        actual = example_source.source_information()
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'
