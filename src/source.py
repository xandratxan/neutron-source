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
        return f'{self.__class__.__name__} source'
