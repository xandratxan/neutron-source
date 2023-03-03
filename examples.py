from src.source import Source, Cf

#  Contents:
#  1. Create your own source modifying generic source attributes
#  2. Create your own source as a new class
#  3. Using example source

#  1. Create your own source modifying generic source attributes
# Create a generic radionuclide neutron source
neutron_source = Source()
# Define neutron source intrinsic characteristics
neutron_source.name = '241-Am/Be'
neutron_source.calibration_date = '2012/01/01'
neutron_source.calibration_strength = (1.11E+07, 1.11E+07 * 0.7 / 100, 0.7)
neutron_source.half_life = (432.6, 0.6, 0.6 / 432.6 * 100)
neutron_source.anisotropy_factor = (1.069, 0.011, 0.011 / 1.069 * 100)
neutron_source.linear_attenuation_coefficient = (890e-7, 890e-7 * 1.5 / 100, 1.5)
neutron_source.fluence_to_dose_conversion_factor = (391, 391 * 4 / 100, 4.0)
neutron_source.neutron_effectiveness = (0.5, 0.1, 0.1 / 0.5 * 100)
neutron_source.total_air_scatter_component = (0.00008, 0.00008 * 15 / 100, 15)
# Print Cf radionuclide neutron source intrinsic characteristics
print(neutron_source)
print()


#  2. Create your own source as a new class
# Define a class which inherits from Source class.
class AmBe(Source):
    """241-Am-Be radionuclide neutron source."""

    def __init__(self):
        super().__init__()
        self.name = '241-Am/Be'
        self.calibration_date = '2012/01/01'
        self.calibration_strength = (1.11E+07, 1.11E+07 * 0.7 / 100, 0.7)
        self.half_life = (432.6, 0.6, 0.6 / 432.6 * 100)
        self.anisotropy_factor = (1.069, 0.011, 0.011 / 1.069 * 100)
        self.linear_attenuation_coefficient = (890e-7, 890e-7 * 1.5 / 100, 1.5)
        self.fluence_to_dose_conversion_factor = (391, 391 * 4 / 100, 4.0)
        self.neutron_effectiveness = (0.5, 0.1, 0.1 / 0.5 * 100)
        self.total_air_scatter_component = (0.00008, 0.00008 * 15 / 100, 15)


# Create a 241-Am/Be radionuclide neutron source
am_be_source = AmBe()
# Print 241-Am/Be radionuclide neutron source
print(am_be_source)
print()

#  3. Using example source
# Create a Cf radionuclide neutron source
cf = Cf()
# Print Cf radionuclide neutron source
print(cf)
print()
# Print Cf radionuclide neutron source intrinsic characteristics
print(cf.source_information())
print()
# Cf radionuclide neutron source characteristics on a specific date
# Compute source decay time on a date
dt = cf.decay_time(date='2020/05/20')
# Compute source decay time on a date
df = cf.decay_factor(final_date='2020/05/20')
# Compute source strength on a date
s = cf.strength(date='2020/05/20')
print(
    f'Initial date: 2012/05/20, final date 2020/05/20\n'
    f'Magnitude (unit): value \u00B1 uncertainty (percentage uncertainty)\n'
    f'Decay time (days): {dt[0]} \u00B1 {dt[1]} ({dt[2]})\n'
    f'Decay factor (non-dimensional): {df[0]} \u00B1 {df[1]} ({df[2]})\n'
    f'Strength (1/s): {s[0]} \u00B1 {s[1]} ({s[2]})'
)
print()
# Compute source decay time between two dates
df2 = cf.decay_factor(final_date='2020/05/20', initial_date='2016/05/20')
print(
    f'Initial date: 2012/05/20, final date 2016/05/20\n'
    f'Decay factor (non-dimensional): {df2[0]} \u00B1 {df2[1]} ({df2[2]})'
)
print()
# Cf radionuclide neutron source characteristics in terms of time and distance
# TODO
# Compute source fluence rate at a distance on a date
fr = cf.fluence_rate(date='2020/05/20', distance=(100, 1, 1))
hr = cf.ambient_dose_equivalent_rate(date='2020/05/20', distance=(100, 1, 1))
print(
    f'Date 2020/05/20, distance 100 cm\n'
    f'Magnitude (unit): value \u00B1 uncertainty (percentage uncertainty)\n'
    f'Fluence rate (1/cm²s): {fr[0]} \u00B1 {fr[1]} ({fr[2]})\n'
    f'Ambient dose equivalent rate (\u03BCSv/h): {hr[0]} \u00B1 {hr[1]} ({hr[2]})\n'
)
