from magnitude import Magnitude

import src.source.equations as eq


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

    # TODO: Representation of non-dimensional magnitudes should be '10 ± 1 (10%)' instead of '10 ± 1 ND (10%)'
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
        tuple
            Source decay time from the source's calibration date (value, uncertainty, percentage uncertainty).
        """
        return eq.elapsed_time(initial_date=self.calibration_date, final_date=date)

    def decay_factor(self, final_date, initial_date=None):
        """Returns the source decay factor and its uncertainty.

        The decay factor is non-dimensional.

        Parameters
        ----------
        initial_date : str
            Initial date to compute the source decay factor.
        final_date : str
            Final date to compute the source decay factor.

        Returns
        -------
        tuple
            Source decay factor between the initial and final dates (value, uncertainty, percentage uncertainty).
        """
        t12, u_t12, ur_t12 = self.half_life
        t12 = t12 * eq.years_to_days
        u_t12 = u_t12 * eq.years_to_days
        if initial_date:
            t, u_t, ur_t = eq.elapsed_time(initial_date=initial_date, final_date=final_date)
        else:
            t, u_t, ur_t = eq.elapsed_time(initial_date=self.calibration_date, final_date=final_date)
        f = eq.decay_factor_value(t=t, t12=t12)
        ur_f = eq.decay_factor_uncertainty(t=t, t12=t12, ur_t=ur_t, ur_t12=ur_t12)
        u_f = eq.absolute_uncertainty(m=f, ur_m=ur_f)
        return f, u_f, ur_f

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
        b0, u_b0, ur_b0 = self.calibration_strength
        t12, u_t12, ur_t12 = self.half_life
        t12 = t12 * eq.years_to_days
        u_t12 = u_t12 * eq.years_to_days
        t, u_t, ur_t = self.decay_time(date=date)
        b = eq.strength_value(b0, t, t12)
        ur_b = eq.strength_relative_uncertainty(t, t12, ur_b0, ur_t, ur_t12)
        u_b = eq.absolute_uncertainty(m=b, ur_m=ur_b)
        return b, u_b, ur_b

    def fluence_rate(self, date, distance):
        # TODO
        pass

    def ambient_dose_equivalent_rate(self, date, distance):
        # TODO
        pass


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
        self.name = '252-Cf radionuclide neutron source'
        self.calibration_date = '2012/05/20'
        self.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.013)
        self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
        self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
        self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
        self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
        self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
        self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)
