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
    calibration_strength : tuple
        Strength of the source at the calibration date in 1/s (value, uncertainty, percentage uncertainty).
    half_life : tuple
        Half life of the source in years (value, uncertainty, percentage uncertainty).
    anisotropy_factor : tuple
        Anisotropy factor of the source, non-dimensional (value, uncertainty, percentage uncertainty).
    linear_attenuation_coefficient : tuple
        Linear attenuation coefficient of the source in 1/cm (value, uncertainty, percentage uncertainty).
    fluence_to_dose_conversion_factor : tuple
        Fluence-to-dose conversion factor of the source in pSv·cm² (value, uncertainty, percentage uncertainty).
    neutron_effectiveness : tuple
        Neutron effectiveness of the source, non-dimensional (value, uncertainty, percentage uncertainty).
    total_air_scatter_component : tuple
        Total air scatter component of the source in 1/cm (value, uncertainty, percentage uncertainty).
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
            f'Magnitude (unit): value \u00B1 uncertainty (percentage uncertainty)\n'
            f'Calibration strength (1/s): '
            f'{self.calibration_strength[0]} \u00B1 '
            f'{self.calibration_strength[1]} '
            f'({self.calibration_strength[2]})\n'
            f'Half life (years): '
            f'{self.half_life[0]} \u00B1 '
            f'{self.half_life[1]} '
            f'({self.half_life[2]})\n'
            f'Anisotropy factor (non-dimensional): '
            f'{self.anisotropy_factor[0]} \u00B1 '
            f'{self.anisotropy_factor[1]} '
            f'({self.anisotropy_factor[2]})\n'
            f'Linear attenuation coefficient (1/cm): '
            f'{self.linear_attenuation_coefficient[0]} \u00B1 '
            f'{self.linear_attenuation_coefficient[1]} '
            f'({self.linear_attenuation_coefficient[2]})\n'
            f'Fluence to dose conversion factor (pSv·cm²): '
            f'{self.fluence_to_dose_conversion_factor[0]} \u00B1 '
            f'{self.fluence_to_dose_conversion_factor[1]} '
            f'({self.fluence_to_dose_conversion_factor[2]})\n'
            f'Neutron effectiveness (non-dimensional): '
            f'{self.neutron_effectiveness[0]} \u00B1 '
            f'{self.neutron_effectiveness[1]} '
            f'({self.neutron_effectiveness[2]})\n'
            f'Total air scatter component (1/cm): '
            f'{self.total_air_scatter_component[0]} \u00B1 '
            f'{self.total_air_scatter_component[1]} '
            f'({self.total_air_scatter_component[2]})'
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
    calibration_strength : tuple
        Strength of the source at the calibration date in 1/s (value, uncertainty, percentage uncertainty):
        :math:`B_0` = 5.471·10\ :sup:`8` s\ :sup:`-1` ± 1.3%.
    half_life : tuple
        Half life of the source in years (value, uncertainty, percentage uncertainty):
        :math:`T_{1/2}` = 2.6470 y ± 0.0026 y.
    anisotropy_factor : tuple
        Anisotropy factor of the source, non-dimensional (value, uncertainty, percentage uncertainty):
        :math:`F_I(\theta)` = 1.051 ± 0.019.
    linear_attenuation_coefficient : tuple
        Linear attenuation coefficient of the source in 1/cm (value, uncertainty, percentage uncertainty):
        :math:`\Sigma` = 1055·10\ :sup:`-7` cm\ :sup:`-1` ± 1,5%.
    fluence_to_dose_conversion_factor : tuple
        Fluence-to-dose conversion factor of the source in pSv·cm² (value, uncertainty, percentage uncertainty):
        :math:`h_\Phi` = 385 pSv·cm\ :sup:`2` ± 1%.
    neutron_effectiveness : tuple
        Neutron effectiveness of the source, non-dimensional (value, uncertainty, percentage uncertainty):
        :math:`\delta` = 0.5 ± 0.1.
    total_air_scatter_component : tuple
        Total air scatter component of the source in 1/cm (value, uncertainty, percentage uncertainty):
        :math:`A` = 1.2% or 0.00012 cm\ :sup:`-1` ± 15%.
    """

    def __init__(self):
        super().__init__()
        self.name = '252-Cf'
        self.calibration_date = '2012/05/20'
        self.calibration_strength = (5.471E+08, 5.471E+08 * 1.3 / 100, 1.3)
        self.half_life = (2.6470, 0.0026, 0.0026 / 2.6470 * 100)
        self.anisotropy_factor = (1.051, 0.019, 0.019 / 1.051 * 100)
        self.linear_attenuation_coefficient = (1055e-7, 1055e-7 * 1.5 / 100, 1.5)
        self.fluence_to_dose_conversion_factor = (385, 385 * 1 / 100, 1)
        self.neutron_effectiveness = (0.5, 0.1, 0.1 / 0.5 * 100)
        self.total_air_scatter_component = (0.00012, 0.00012 * 15 / 100, 15)
