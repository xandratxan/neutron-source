"""
Module to work with calibration radionuclide neutron sources and conventional true values of quantities of interest.

Classes
-------
Source :
    Class to represent a generic calibration radionuclide neutron source.
Cf :
    Class to represent an example calibration radionuclide neutron source.

Data
----
time_uncertainty_days : int
    Uncertainty of time, set to 1 day by convention.
conversion_years_to_days : float
    Conversion factor for time from years to days set to 365.242 without uncertainty.
conversion_psv_s_to_usv_h : Magnitude
    Conversion factor for equivalent dose from pSv/s to uSv/h set to 0.0036 without uncertainty.
standard_units : dict
    Dictionary of the units used by convention for radionuclide neutron source related magnitudes.
    Calibration strength in 1/s, half life in years, linear attenuation coefficient in 1/cm,
    fluence-to-dose conversion factor in pSv·cm², total air scatter component in 1/cm, decay time in days,
    strength in 1/s, fluence rate in 1/cm²s and ambient dose equivalent rate in uSv/h.
"""
from copy import copy
from datetime import datetime
from math import exp, log, sqrt
from math import pi

from magnitude import Magnitude

time_uncertainty_days = 1
conversion_years_to_days = 365.242
conversion_psv_s_to_usv_h = Magnitude(value=0.0036, unit='uSv·s/pSv/h', uncertainty=0)
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
    Class to represent a generic calibration radionuclide neutron source.

    Attributes
    ----------
    name : str
        Name of the source.
    calibration_date : str
        Date of calibration of the source.
    calibration_strength : Magnitude
        Strength of the source at the calibration date in 1/s.
    half_life : Magnitude
        Half life of the source in years.
    anisotropy_factor : Magnitude
        Anisotropy factor of the source, non-dimensional.
    linear_attenuation_coefficient : Magnitude
        Linear attenuation coefficient of the source in 1/cm.
    fluence_to_dose_conversion_factor : Magnitude
        Fluence-to-dose conversion factor of the source in pSv·cm².
    neutron_effectiveness : Magnitude
        Neutron effectiveness of the source, non-dimensional.
    total_air_scatter_component : Magnitude
        Total air scatter component of the source in 1/cm.

    Raises
    -------
    ValueError
        If the value of any attribute is negative.
    ValueError
        If the uncertainty of any attribute is negative.
    ValueError
        If the relative uncertainty of any attribute is negative.
    ValueError
        If the unit of any attribute doesn't comply with package unit convention.
    """

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
        """Check consistency when an attribute assignment is attempted."""
        self.__dict__[name] = value
        if name in self.numeric_attributes():
            self.check_consistency(attr=name)

    def numeric_attributes(self):
        """Returns a dictionary mapping the attributes of a ``Source`` object of type Magnitude.

        Returns
        -------
        attributes : dict
            Dictionary mapping the attributes of a Source object of type Magnitude
        """
        attributes = {}
        for attr, magnitude in self.__dict__.items():
            if attr != 'name' and attr != 'calibration_date':
                attributes[attr] = magnitude
        return attributes

    def check_consistency(self, attr):
        """Check the consistency of an attributes of a ``Source`` object of type Magnitude in terms of physical meaning.

        The ``Magnitude`` value, uncertainty and relative uncertainty must be a positive number.
        The ``Magnitude`` unit must comply with package unit convention.

        Parameters
        ----------
        attr : str
            Name of the attribute of the ``Source`` object.
        """

        # All numeric values and uncertainties must be positive
        # All units must be standard
        magnitude = self.__dict__[attr]
        if magnitude is not None:
            if magnitude.value < 0:
                raise ValueError(f'Source {attr} value must be positive.')
            if magnitude.uncertainty < 0:
                raise ValueError(f'Source {attr} uncertainty must be positive.')
            if magnitude.relative_uncertainty < 0:
                raise ValueError(f'Source {attr} relative uncertainty must be positive.')
            if magnitude.unit != standard_units[attr]:
                raise ValueError(f'Source {attr} units must be standard.')

    def decay_time(self, date):
        """Compute the source's decay time on a ``date`` from the calibration date.

        It is computed as the difference between the source's calibration date and
        the desired date at which decay time is to be computed.
        The unit of the elapsed time is day.
        Standard uncertainty of the elapsed time is assumed to be 1 day.
        Relative standard uncertainty is computed by uncertainty propagation.

        Parameters
        ----------
        date : str
            Date on which decay time is to be computed.

        Returns
        -------
        Magnitude
            Source's decay time on a ``date`` from the calibration date.
        """
        t = _elapsed_time(initial_date=self.calibration_date, final_date=date)
        return Magnitude(value=t, unit='d', uncertainty=time_uncertainty_days)

    def decay_factor(self, date):
        """Compute the source's decay factor on a ``date`` from the calibration date.

        The decay factor is non-dimensional.
        Its value is computed as:

        .. math::
            f=e^{-\\frac{\\ln(2)t}{t_{12}}}

        where :math:`t` the source's decay time from the source's calibration date and
        :math:`t_{1/2}` if the source's half life.
        Standard uncertainty and relative standard uncertainty are computed by uncertainty propagation.
        Its relative standard uncertainty is computed as:

        .. math::
            u_r(f)=\\sqrt{\\left(\\frac{\\ln(2)t}{t_{12}}\\right)^2\\left(u_r^2(t)+u_r^2(t_{1/2})\\right)}

        Parameters
        ----------
        date : str
            Date on which decay factor is to be computed.

        Returns
        -------
        Magnitude
            Source's decay factor on a ``date`` from the calibration date.
        """
        # TODO: compute decay factor value and uncertainty using Magnitudes
        t12 = copy(self.half_life)
        t12.value = t12.value * conversion_years_to_days
        t = self.decay_time(date=date)
        f = _decay_factor_value(t=t.value, t12=t12.value)
        ur_f = _decay_factor_uncertainty(t=t.value, t12=t12.value,
                                         ur_t=t.relative_uncertainty, ur_t12=t12.relative_uncertainty)
        return Magnitude(value=f, unit='ND', relative_uncertainty=ur_f)

    def strength(self, date):
        """Compute the source's strength on a ``date`` from the calibration date.

        The unit of the strength is 1/s.
        Its value is computed as:

        .. math::
            B=B_0f

        where :math:`B_0` is the source's strength on the source's calibration date and
        :math:`f` is the source's decay factor.
        Standard uncertainty and relative standard uncertainty are computed by uncertainty propagation.
        If the specified date is the source's calibration date, return the source's calibration strength.

        Parameters
        ----------
        date : str
            Date on which source strength is to be computed.

        Returns
        -------
        Magnitude
            Source's strength on a ``date`` from the calibration date.
        """
        if date == self.calibration_date:
            return self.calibration_strength
        else:
            b = self.calibration_strength * self.decay_factor(date=date)
            b.unit = '1/s'
            return b

    def fluence_rate(self, date, distance):
        """Compute the source's fluence rate on a ``date`` from the calibration date at a ``distance`` from the source.

        The unit of the fluence rate is 1/cm²s.
        Its value is computed as:

        .. math::
            \\varphi=\\frac{Bf_I}{4\\pi l^2}

        where :math:`B` is the source's strength, :math:`f_I` is the source's anisotropy factor
        and :math:`l` is the distance from the source.
        Standard uncertainty and relative standard uncertainty are computed by uncertainty propagation.
        Its relative standard uncertainty is computed as:

        .. math::
            u_r(\\varphi)=\\sqrt{u_r(B)^2+u_r(f_I)^2+u_r(l)^2}

        Parameters
        ----------
        date : str
            Date on which source's fluence rate is to be computed.
        distance : Magnitude
            Distance at which source's fluence rate is to be computed.

        Returns
        -------
        Magnitude
            Source's fluence rate on a ``date`` from the calibration date at a ``distance`` from the source.
        """
        b = self.strength(date=date)
        fi = self.anisotropy_factor
        _pi = Magnitude(value=pi, unit='ND', uncertainty=0)
        _4 = Magnitude(value=4, unit='ND', uncertainty=0)
        f = b * fi / _4 / _pi / distance / distance
        f.unit = '1/cm²s'
        return f

    def ambient_dose_equivalent_rate(self, date, distance):
        """Compute the source's ambient dose equivalent rate on a ``date`` from the calibration date
        at a ``distance`` from the source.

        The unit of the ambient dose equivalent rate is \u00B5 /h.
        Its value is computed as:

        .. math::
            \\H^*(10)=h_{\\varphi}\\varphi

        where :math:`\\varphi` is the source's fluence rate and
        :math:`h_{\\varphi}` is fluence-to-dose conversion coefficient.
        Standard uncertainty and relative standard uncertainty are computed by uncertainty propagation.
        Its relative standard uncertainty is computed as:

        .. math::
            u_r(H^*(10))=\\sqrt{u_r(\\varphi)^2+u_r(h_{\\varphi})^2}

        Parameters
        ----------
        date : str
            Date on which source's ambient dose equivalent rate is to be computed.
        distance : Magnitude
            Distance at which source's ambient dose equivalent rate is to be computed.

        Returns
        -------
        Magnitude
            Source's ambient dose equivalent rate on a ``date`` from the calibration date
            at a ``distance`` from the source.
        """
        hf = self.fluence_to_dose_conversion_factor
        f = self.fluence_rate(date=date, distance=distance)
        h = hf * f * conversion_psv_s_to_usv_h
        h.unit = 'uSv/h'
        return h


class Cf(Source):
    """
    Class to represent an example calibration radionuclide neutron source.

    Attributes
    ----------
    name : str
        Name of the source: 252-Cf.
    calibration_date : str
        Calibration date of the source: 2012-05-20.
    calibration_strength : Magnitude
        Strength of the source at the calibration date:
        :math:`B_0 = 5.471·10^8\\ s^{-1} ± 1.3\\%`.
    half_life : Magnitude
        Half life of the source:
        :math:`T_{1/2} = 2.6470\\ y ± 0.0026 y`.
    anisotropy_factor : Magnitude
        Anisotropy factor of the source:
        :math:`F_I(\\theta) = 1.051 ± 0.019`.
    linear_attenuation_coefficient : Magnitude
        Linear attenuation coefficient of the source:
        :math:`\\Sigma = 1055·10^{-7}\\ cm^{-1} ± 1.5\\%`.
    fluence_to_dose_conversion_factor : Magnitude
        Fluence-to-dose conversion factor of the source:
        :math:`h_{\\Phi} = 385\\ pSv·cm^2 ± 1\\%`.
    neutron_effectiveness : Magnitude
        Neutron effectiveness of the source:
        :math:`\\delta = 0.5 ± 0.1`.
    total_air_scatter_component : Magnitude
        Total air scatter component of the source:
        :math:`A = 0.00012\\ cm^{-1} ± 15\\%`.
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


def _elapsed_time(initial_date, final_date):
    """Compute the elapsed time between two dates in days.

    Parameters
    ----------
    initial_date : str
        Initial date to compute the elapsed time.
    final_date : str
        Final date to compute the elapsed time.

    Returns
    -------
    float
        Elapsed time between two dates in days.
    """
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    t = final_date - initial_date
    t = t.days
    return t


def _decay_factor_value(t, t12):
    """Compute the value of the source's decay factor on a date from the calibration date.

    Its value is computed as:

    .. math::
        f=e^{-\\frac{\\ln(2)t}{t_{12}}}

    where :math:`t` the source's decay time from the source's calibration date and
    :math:`t_{1/2}` if the source's half life.

    Parameters
    ----------
    t : int or float
        Value of source's decay time.
    t12 : int or float
        Value of source's half life.

    Returns
    -------
    float
        Value of source's decay factor on a date from the calibration date.
    """
    return exp(-log(2) * t / t12)


def _decay_factor_uncertainty(t, t12, ur_t, ur_t12):
    """Compute relative standard uncertainty of the source's decay factor on a date from the calibration date.

    Its relative standard uncertainty is computed as:

    .. math::
        u_r(f)=\\sqrt{\\left(\\frac{\\ln(2)t}{t_{12}}\\right)^2\\left(u_r^2(t)+u_r^2(t_{1/2})\\right)}

    Parameters
    ----------
    t : int or float
        Value of source's decay time.
    t12 : int or float
        Value of source's half life.
    ur_t : int or float
        Relative uncertainty of source's decay time.
    ur_t12 : int or float
        Relative uncertainty of source's half life.

    Returns
    -------
    float
        Relative standard uncertainty of source's decay factor on a date from the calibration date.
    """
    return sqrt((log(2) * t / t12) ** 2 * (ur_t ** 2 + ur_t12 ** 2))

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
