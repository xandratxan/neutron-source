from copy import copy
from math import pi

from magnitude import Magnitude

import src.source.equations as eq

u_t_days = 1  # TODO rename uncertainty_
years_to_days = 365.242  # TODO rename conversion_
psv_s_to_usv_h = Magnitude(value=0.0036, unit='uSv·s/pSv/h', uncertainty=0)  # TODO rename conversion_
standard_units = {
    'calibration_strength': '1/s',
    'half_life': 'y',
    'anisotropy_factor': 'ND',
    'linear_attenuation_coefficient': '1/cm',
    'fluence_to_dose_conversion_factor': 'pSv·cm²',
    'neutron_effectiveness': 'ND',
    'total_air_scatter_component': '1/cm'
}


class Source:
    """
    Generic radionuclide neutron source.

    Attributes
    ----------
    name : str
        Name of the source.
    calibration_date : str
        Date of calibration of the source.
    calibration_strength : Magnitude
        Strength of the source at the calibration date in 1/s (value and absolute or relative uncertainty).
    half_life : Magnitude
        Half life of the source in years (value and absolute or relative uncertainty).
    anisotropy_factor : Magnitude
        Anisotropy factor of the source, non-dimensional (value and absolute or relative uncertainty).
    linear_attenuation_coefficient : Magnitude
        Linear attenuation coefficient of the source in 1/cm (value and absolute or relative uncertainty).
    fluence_to_dose_conversion_factor : Magnitude
        Fluence-to-dose conversion factor of the source in pSv·cm² (value and absolute or relative uncertainty).
    neutron_effectiveness : Magnitude
        Neutron effectiveness of the source, non-dimensional (value and absolute or relative uncertainty).
    total_air_scatter_component : Magnitude
        Total air scatter component of the source in 1/cm (value and absolute or relative uncertainty).
    """

    # TODO: check docstrings
    # TODO: Check units of source characteristics

    def __init__(self):
        self.name = self.__class__.__name__
        self.calibration_date = None
        self.calibration_strength = None
        self.half_life = None
        self.anisotropy_factor = None
        self.linear_attenuation_coefficient = None
        self.fluence_to_dose_conversion_factor = None
        self.neutron_effectiveness = None
        self.total_air_scatter_component = None

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}()'

    def __str__(self):
        return f'{self.name} radionuclide neutron source'

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name in self.numeric_attributes():
            self.check_consistency(attr=name)

    def numeric_attributes(self):
        for attr, magnitude in self.__dict__.items():
            if attr != 'name' and attr != 'calibration_date':
                yield attr, magnitude

    def check_consistency(self, attr):
        # All numeric values and uncertainties must be positive
        # All units must be standard
        magnitude = self.__dict__[attr]
        if magnitude is not None:
            if magnitude.value < 0:
                raise ValueError(f'Source {attr} value must be positive.')
            elif magnitude.uncertainty < 0:
                raise ValueError(f'Source {attr} uncertainty must be positive.')
            elif magnitude.relative_uncertainty < 0:
                raise ValueError(f'Source {attr} relative uncertainty must be positive.')
            elif magnitude.unit != standard_units[attr]:
                raise ValueError(f'Source {attr} units must be standard.')

        # for attr, magnitude in self.numeric_attributes():
        #     if magnitude is not None:
        #         if magnitude.value < 0:
        #             raise ValueError(f'Source {attr} value must be positive.')
        #         elif magnitude.uncertainty < 0:
        #             raise ValueError(f'Source {attr} uncertainty must be positive.')
        #         elif magnitude.relative_uncertainty < 0:
        #             raise ValueError(f'Source {attr} relative uncertainty must be positive.')
        #         elif magnitude.unit != standard_units[attr]:
        #             raise ValueError(f'Source {attr} units must be standard.')

    def source_information(self):
        """Returns the source characteristics.

        Returns
        -------
        str
            String containing the source characteristics.
        """
        return (
            f'Name: {self.name}\n'
            f'Calibration date: {self.calibration_date}\n'
            f'Magnitude: value \u00B1 uncertainty (percentage uncertainty)\n'
            f'Calibration strength: {self.calibration_strength}\n'
            f'Half life: {self.half_life}\n'
            f'Anisotropy factor: {self.anisotropy_factor}\n'
            f'Linear attenuation coefficient: {self.linear_attenuation_coefficient}\n'
            f'Fluence to dose conversion factor: {self.fluence_to_dose_conversion_factor}\n'
            f'Neutron effectiveness: {self.neutron_effectiveness}\n'
            f'Total air scatter component: {self.total_air_scatter_component}'
        )

    def decay_time(self, date):
        """Returns the source decay time and its uncertainty.

        The unit of the elapsed time is day.
        Standard uncertainty of the elapsed time is assumed to be 1 day.

        Parameters
        ----------
        date : str
            Date to compute the elapsed time.

        Returns
        -------
        Magnitude
            Source decay time from the source's calibration date (value, uncertainty, percentage uncertainty).
        """
        t = eq.elapsed_time(initial_date=self.calibration_date, final_date=date)
        return Magnitude(value=t, unit='d', uncertainty=u_t_days)

    def decay_factor(self, date):
        """Returns the source decay factor and its uncertainty.

        The decay factor is non-dimensional.

        Parameters
        ----------
        date : str
            Final date to compute the source decay factor.

        Returns
        -------
        Magnitude
            Source decay factor from the source's calibration date (value, uncertainty, percentage uncertainty).
        """
        # TODO: compute decay factor value and uncertainty using Magnitudes
        t12 = copy(self.half_life)
        t12.value = t12.value * years_to_days
        t = self.decay_time(date=date)
        f = eq.decay_factor_value(t=t.value, t12=t12.value)
        ur_f = eq.decay_factor_uncertainty(t=t.value, t12=t12.value,
                                           ur_t=t.relative_uncertainty, ur_t12=t12.relative_uncertainty)
        return Magnitude(value=f, unit='ND', relative_uncertainty=ur_f)

    def strength(self, date):
        """Returns the source strength at the specified date and its uncertainty.

        The unit of the strength is 1/s.
        If date is the source's calibration date, return the source's calibration strength.

        Parameters
        ----------
        date : str
            Date to compute the source strength.

        Returns
        -------
        tuple
            Source strength at the specified date, in 1/s (value, uncertainty, percentage uncertainty).
        """
        if date == self.calibration_date:
            return self.calibration_strength
        else:
            b = self.calibration_strength * self.decay_factor(date=date)
            b.unit = '1/s'
            return b

    def fluence_rate(self, date, distance):
        b = self.strength(date=date)
        fi = self.anisotropy_factor
        l = distance
        _pi = Magnitude(value=pi, unit='ND', uncertainty=0)
        _4 = Magnitude(value=4, unit='ND', uncertainty=0)
        f = b * fi / _4 / _pi / l / l
        f.unit = '1/cm²s'
        return f

    def ambient_dose_equivalent_rate(self, date, distance):
        hf = self.fluence_to_dose_conversion_factor
        f = self.fluence_rate(date=date, distance=distance)
        h = hf * f * psv_s_to_usv_h
        h.unit = 'uSv/h'
        return h


class Cf(Source):
    """252-Cf radionuclide neutron source from LPN.

    Attributes
    ----------
    calibration_date : str
        Date of calibration of the source: 2012-05-20.
    calibration_strength : Magnitude
        Strength of the source at the calibration date in 1/s (value and absolute or relative uncertainty).
        :math:`B_0` = 5.471·10\ :sup:`8` s\ :sup:`-1` ± 1.3%.
    half_life : Magnitude
        Half life of the source in years (value and absolute or relative uncertainty).
        :math:`T_{1/2}` = 2.6470 y ± 0.0026 y.
    anisotropy_factor : Magnitude
        Anisotropy factor of the source, non-dimensional (value and absolute or relative uncertainty).
        :math:`F_I(\theta)` = 1.051 ± 0.019.
    linear_attenuation_coefficient : Magnitude
        Linear attenuation coefficient of the source in 1/cm (value and absolute or relative uncertainty).
        :math:`\Sigma` = 1055·10\ :sup:`-7` cm\ :sup:`-1` ± 1,5%.
    fluence_to_dose_conversion_factor : Magnitude
        Fluence-to-dose conversion factor of the source in pSv·cm² (value and absolute or relative uncertainty).
        :math:`h_\Phi` = 385 pSv·cm\ :sup:`2` ± 1%.
    neutron_effectiveness : Magnitude
        Neutron effectiveness of the source, non-dimensional (value and absolute or relative uncertainty).
        :math:`\delta` = 0.5 ± 0.1.
    total_air_scatter_component : Magnitude
        Total air scatter component of the source in 1/cm (value and absolute or relative uncertainty).
        :math:`A` = 1.2% or 0.00012 cm\ :sup:`-1` ± 15%.
    """

    def __init__(self):
        super().__init__()
        self.name = '252-Cf'
        self.calibration_date = '2012/05/20'
        self.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.013)
        self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
        self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
        self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
        self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
        self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
        self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)

# TODO: Script to automate tests expected values
# TODO: Sphinx documentation
# TODO: Update README
# TODO: Emulate Ri pull request

# TODO: BUG1 Magnitudes, representation, non-dimensional magnitudes, from '10 ± 1 ND (10%)' to '10 ± 1 (10%)'
# TODO: Magnitudes: add parenthesis to units product and division.
#  Check all magnitudes (check print(h.unit) before unit conversion)
# TODO: Magnitudes, representation, show only significant numbers
# TODO: Magnitudes, tests, script to automate tests expected values
# TODO: BUG2 Magnitudes, negative values cant be defined since uncertainty calculation will derive negative uncertainty!
#  Magnitude(value=-2.6470, unit='y', uncertainty=0.0026) This should be possible
#  Magnitude(value=-2.6470, unit='y', uncertainty=-0.0026) This should not be possible
# TODO: BUG3 Magnitudes, assign negative value to uncertainty attributes should not be possible
#  m = Magnitude(value=10, unit='m', uncertainty=1)
#  m.uncertainty = -1
#  m.relative_uncertainty = -1
