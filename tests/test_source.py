import pytest
from magnitude import Magnitude

from src.source.source import Source, Cf


@pytest.fixture
def source():
    return Cf()


class TestSourceAttributesValue:
    def test_source_representation(self, source):
        expected = 'src.source.source.Cf()'
        actual = source.__repr__()
        assert actual == expected, f'Source representation should be {expected}, not {actual}.'

    def test_source_string(self, source):
        expected = '252-Cf radionuclide neutron source'
        actual = str(source)
        assert actual == expected, f'Source string should be {expected}, not {actual}.'

    def test_source_calibration_date(self, source):
        expected = '2012/05/20'
        actual = source.calibration_date
        assert actual == expected, f'Source calibration date should be {expected}, not {actual}.'

    def test_source_calibration_strength(self, source):
        expected = f'547100000.0 ± {5.471E+08 * 1.3 / 100} 1/s (1.3%)'
        actual = str(source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_source_half_life(self, source):
        expected = f'2.647 ± 0.0026 y ({0.0026 / 2.6470 * 100}%)'
        actual = str(source.half_life)
        assert actual == expected, f'Source half life should be {expected}, not {actual}.'

    def test_source_anisotropy_factor(self, source):
        expected = f'1.051 ± 0.019 ND ({0.019 / 1.051 * 100}%)'
        actual = str(source.anisotropy_factor)
        assert actual == expected, f'Source anisotropy factor should be {expected}, not {actual}.'

    def test_source_linear_attenuation_coefficient(self, source):
        expected = f'0.0001055 ± {1055e-7 * 1.5 / 100} 1/cm (1.5%)'
        actual = str(source.linear_attenuation_coefficient)
        assert actual == expected, f'Source linear attenuation coefficient should be {expected}, not {actual}.'

    def test_source_fluence_to_dose_conversion_factor(self, source):
        expected = f'385 ± {385 * 1 / 100} pSv·cm² (1.0%)'
        actual = str(source.fluence_to_dose_conversion_factor)
        assert actual == expected, f'Source fluence-to-dose conversion factor should be {expected}, not {actual}.'

    def test_source_neutron_effectiveness(self, source):
        expected = f'0.5 ± 0.1 ND ({0.1 / 0.5 * 100}%)'
        actual = str(source.neutron_effectiveness)
        assert actual == expected, f'Source neutron effectiveness should be {expected}, not {actual}.'

    def test_source_total_air_scatter_component(self, source):
        expected = f'0.00012 ± {0.00012 * 15 / 100} 1/cm (15.0%)'
        actual = str(source.total_air_scatter_component)
        assert actual == expected, f'Source total air scatter component should be {expected}, not {actual}.'


class TestSourceAttributesConsistency:
    def test_all_values_positive(self, source):
        attributes = source.numeric_attributes()
        for attr, magnitude in attributes.items():
            assert magnitude.value >= 0, f'Source {attr} value must be positive.'

    def test_all_uncertainties_positive(self, source):
        attributes = source.numeric_attributes()
        for attr, magnitude in attributes.items():
            assert magnitude.uncertainty >= 0, f'Source {attr} value must be positive.'

    def test_all_relative_uncertainties_positive(self, source):
        attributes = source.numeric_attributes()
        for attr, magnitude in attributes.items():
            assert magnitude.uncertainty >= 0, f'Source {attr} value must be positive.'

    def test_all_units_standard(self, source):
        assert source.calibration_strength.unit == '1/s'
        assert source.half_life.unit == 'y'
        assert source.anisotropy_factor.unit == 'ND'
        assert source.linear_attenuation_coefficient.unit == '1/cm'
        assert source.fluence_to_dose_conversion_factor.unit == 'pSv·cm²'
        assert source.neutron_effectiveness.unit == 'ND'
        assert source.total_air_scatter_component.unit == '1/cm'

    def test_class_assignment_negative_value(self):
        with pytest.raises(ValueError) as exc:
            class MySource(Source):
                def __init__(self):
                    super().__init__()
                    self.name = '252-Cf'
                    self.calibration_date = '2012/05/20'
                    self.calibration_strength = Magnitude(value=-5.471E+08, unit='1/s', relative_uncertainty=0.013)
                    self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
                    self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
                    self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm',
                                                                    relative_uncertainty=0.015)
                    self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²',
                                                                       relative_uncertainty=0.01)
                    self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
                    self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)

            MySource()
        assert 'Source calibration strength must be positive.' in str(exc.value)

    def test_class_assignment_negative_uncertainty(self):
        with pytest.raises(ValueError) as exc:
            class MySource(Source):
                def __init__(self):
                    super().__init__()
                    self.name = '252-Cf'
                    self.calibration_date = '2012/05/20'
                    self.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=-0.013)
                    self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
                    self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
                    self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm',
                                                                    relative_uncertainty=0.015)
                    self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²',
                                                                       relative_uncertainty=0.01)
                    self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
                    self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)

            MySource()
        assert 'Uncertainties must be positive.' in str(exc.value)

    def test_class_assignment_non_standard_unit(self):
        with pytest.raises(ValueError) as exc:
            class MySource(Source):
                def __init__(self):
                    super().__init__()
                    self.name = '252-Cf'
                    self.calibration_date = '2012/05/20'
                    self.calibration_strength = Magnitude(value=5.471E+08, unit='s', relative_uncertainty=0.013)
                    self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
                    self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
                    self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm',
                                                                    relative_uncertainty=0.015)
                    self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²',
                                                                       relative_uncertainty=0.01)
                    self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
                    self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)

            MySource()
        assert 'Source calibration_strength units must be standard.' in str(exc.value)

    def test_magnitude_assignment_negative_value(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength = Magnitude(value=-5.471E+08, unit='1/s', relative_uncertainty=0.013)
        assert 'Source calibration strength must be positive.' in str(exc.value)

    def test_magnitude_assignment_non_standard_unit(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength = Magnitude(value=5.471E+08, unit='s', relative_uncertainty=0.013)
        assert 'Source calibration_strength units must be standard.' in str(exc.value)

    def test_magnitude_assignment_negative_uncertainty(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=-0.013)
        assert 'Uncertainties must be positive.' in str(exc.value)

    def test_magnitude_assignment_modified_value(self, source):
        source.calibration_strength = Magnitude(value=5.471E+07, unit='1/s', relative_uncertainty=0.013)
        expected = f'54710000.0 ± {5.471E+07 * 0.013} 1/s (1.3%)'
        actual = str(source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_magnitude_assignment_modified_uncertainty(self, source):
        source.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.02)
        expected = f'547100000.0 ± {5.471E+08 * 0.02} 1/s (2.0%)'
        actual = str(source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_magnitude_attribute_assignment_negative_value(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength.value = -5.471E+08
        assert 'Source calibration strength must be positive.' in str(exc.value)

    def test_magnitude_attribute_assignment_negative_uncertainty(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength.relative_uncertainty = -0.013
        assert 'Uncertainties must be positive.' in str(exc.value)

    def test_magnitude_attribute_assignment_non_standard_unit(self, source):
        with pytest.raises(ValueError) as exc:
            source.calibration_strength.units = 's'
        assert 'Source calibration_strength units must be standard.' in str(exc.value)

    def test_magnitude_attribute_assignment_modified_value(self, source):
        source.calibration_strength.value = 5.471E+07
        expected = f'54710000.0 ± {5.471E+07 * 0.013} 1/s (1.3%)'
        actual = str(source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'

    def test_magnitude_attribute_assignment_modified_uncertainty(self, source):
        source.calibration_strength.relative_uncertainty = 0.02
        expected = f'547100000.0 ± {5.471E+08 * 0.02} 1/s (2.0%)'
        actual = str(source.calibration_strength)
        assert actual == expected, f'Source calibration strength should be {expected}, not {actual}.'


class TestSourceMethods:
    date = '2020/05/20'
    distance = Magnitude(value=100, unit='cm', uncertainty=1)

    def test_decay_time(self, source):
        expected = f'2922 ± 1 d ({1 / 2922 * 100}%)'
        actual = str(source.decay_time(date=self.date))
        assert actual == expected, f'Source decay time should be {expected}, not {actual}.'

    def test_decay_factor(self, source):
        expected = f'0.12307796649188105 ± 0.0002681946089174612 ND (0.21790627239129182%)'
        actual = str(source.decay_factor(date=self.date))
        assert actual == expected, f'Source decay factor should be {expected}, not {actual}.'

    def test_source_strength(self, source):
        expected = f'67335955.46770813 ± 887579.6306368469 1/s (1.3181362386140014%)'
        actual = str(source.strength(date=self.date))
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

    def test_source_strength_at_calibration_date(self, source):
        expected = source.calibration_strength
        actual = source.strength(date=source.calibration_date)
        assert actual == expected, f'Source strength should be {expected}, not {actual}.'

    def test_fluence_rate(self, source):
        expected = f'563.170475934353 ± 14.906082662095244 1/cm²s (2.6468153603692817%)'
        actual = str(source.fluence_rate(date=self.date, distance=self.distance))
        assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'

    def test_ambient_dose_equivalent_rate(self, source):
        expected = f'780.5542796450133 ± 22.085178231439247 uSv/h (2.8294224767409286%)'
        actual = str(source.ambient_dose_equivalent_rate(date=self.date, distance=self.distance))
        assert actual == expected, f'Source fluence rate should be {expected}, not {actual}.'

# TODO: validate numbers
# TODO: Script to automate tests expected values
