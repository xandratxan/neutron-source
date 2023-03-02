from datetime import datetime

time_uncertainty_days = 1


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
        return f'{self.name} source'

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
        return elapsed_time(self.calibration_date, date)


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
        self.anisotropy_factor = (1.051, 0.019, 0.019 / 1.051 * 100)  # DT-LMRI-2201
        self.linear_attenuation_coefficient = (1055e-7, 1055e-7 * 1.5 / 100, 1.5)
        self.fluence_to_dose_conversion_factor = (385, 385 * 1 / 100, 1)
        self.neutron_effectiveness = (0.5, 0.1, 0.1 / 0.5 * 100)
        self.total_air_scatter_component = (0.00012, 0.00012 * 15 / 100, 15)


def elapsed_time(initial_date, final_date):
    """Returns the elapsed time between two dates and its uncertainty.

    The unit of the elapsed time is day.
    Standard uncertainty of the elapsed time is assumed to be 1 day.

    Parameters
    ----------
    initial_date : str
        Initial date to compute the elapsed time.
    final_date : str
        Final date to compute the elapsed time.

    Returns
    -------
    tuple
        Elapsed time between the initial and final dates (value, uncertainty, percentage uncertainty).
    """
    # TODO: this method may be in a separate module, it is not a characteristic of a neutron source
    initial_date = datetime.strptime(initial_date, '%Y/%m/%d')
    final_date = datetime.strptime(final_date, '%Y/%m/%d')
    time = final_date - initial_date
    time = time.days
    uncertainty = time_uncertainty_days
    percentage = percentage_uncertainty(time, uncertainty)
    return time, uncertainty, percentage


def percentage_uncertainty(value, absolute_uncertainty):
    """Returns the percentage uncertainty of a magnitude from its absolute uncertainty.

    Parameters
    ----------
    value : num
        Value of the magnitude.
    absolute_uncertainty : num
        Absolute uncertainty of the magnitude.

    Returns
    -------
    num
        Percentage uncertainty of the magnitude.
    """
    # TODO: this method may be in a separate module, it is not a characteristic of a neutron source
    return absolute_uncertainty / value * 100
