from magnitude import Magnitude

from src.source.source import Source, Cf

#  Contents:
#  1. Create your own source modifying generic source attributes
#  2. Create your own source as a new class
#  3. Using example source
#  4. Consistency check

#  1. Create your own source modifying generic source attributes
# ----------------------------------------------------------------------------------------------------------------------
# Create a generic radionuclide neutron source
neutron_source = Source()
# Define neutron source intrinsic characteristics
neutron_source.name = '252-Cf'
neutron_source.calibration_date = '2012/05/20'
neutron_source.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.013)
neutron_source.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
neutron_source.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
neutron_source.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
neutron_source.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
neutron_source.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
neutron_source.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)
# Print Cf radionuclide neutron source intrinsic characteristics
print(neutron_source)


#  2. Create your own source as a new class
# ----------------------------------------------------------------------------------------------------------------------
# Define a class which inherits from Source class.
class MySource(Source):
    """252-Cf radionuclide neutron source from LPN."""

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


# Create a 241-Am/Be radionuclide neutron source
my_source = MySource()
# Print 241-Am/Be radionuclide neutron source
print(my_source)

#  3. Using example source
# ----------------------------------------------------------------------------------------------------------------------
# Create a Cf radionuclide neutron source
cf = Cf()
# Print Cf radionuclide neutron source
print(cf)
# Print Cf radionuclide neutron source intrinsic characteristics
print(cf.source_information())
# Cf radionuclide neutron source characteristics on a specific date
date = '2020/05/20'
print(f'Date: {date}')
# Compute source decay time on a date
dt = cf.decay_time(date=date)
print(dt)
# Compute source decay time on a date
df = cf.decay_factor(date=date)
print(df)
# Compute source strength on a date
s = cf.strength(date=date)
print(s)
# Cf radionuclide neutron source characteristics in terms of time and distance
distance = Magnitude(value=100, unit='cm', uncertainty=1)
print(f'Date: {date}, Distance: {distance}')
# Compute source fluence rate at a distance on a date
fr = cf.fluence_rate(date=date, distance=distance)
print(fr)
# Compute source ambient dose equivalent rate at a distance on a date
hr = cf.ambient_dose_equivalent_rate(date=date, distance=distance)
print(hr)

#  4. Consistency checks
# ----------------------------------------------------------------------------------------------------------------------
# Access to numeric attributes
for attr, magnitude in cf.numeric_attributes():
    print(attr, magnitude)

# Check consistency: Different ways to define or assign a different value to an attribute:

# 4.1. Defining a Class(Source):
# ----------------------------------------------------------------------------------------------------------------------


# with attribute with negative value
try:
    class MySource(Source):
        """252-Cf radionuclide neutron source from LPN."""

        def __init__(self):
            super().__init__()
            self.name = '252-Cf'
            self.calibration_date = '2012/05/20'
            self.calibration_strength = Magnitude(value=-5.471E+08, unit='1/s', relative_uncertainty=0.013)
            self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
            self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
            self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
            self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
            self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
            self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)


    my_source = MySource()
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# raises ValueError: Uncertainties must be positive.
# expected ValueError: Source calibration strength must be positive.
# TODO FAIL


# with attribute with non-standard units
try:
    class MySource(Source):
        """252-Cf radionuclide neutron source from LPN."""

        def __init__(self):
            super().__init__()
            self.name = '252-Cf'
            self.calibration_date = '2012/05/20'
            self.calibration_strength = Magnitude(value=5.471E+08, unit='s', relative_uncertainty=0.013)
            self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
            self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
            self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
            self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
            self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
            self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)


    my_source = MySource()
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# OK raises ValueError: Source calibration_strength units must be standard.


# with negative uncertainty
try:
    class MySource(Source):
        """252-Cf radionuclide neutron source from LPN."""

        def __init__(self):
            super().__init__()
            self.name = '252-Cf'
            self.calibration_date = '2012/05/20'
            self.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=-0.013)
            self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
            self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
            self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
            self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
            self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
            self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)


    my_source = MySource()
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# OK raise ValueError: Uncertainties must be positive.

# 4.2. Assigning a Magnitude to attribute
# ----------------------------------------------------------------------------------------------------------------------
try:
    cf = Cf()
    cf.calibration_strength = Magnitude(value=-5.471E+08, unit='1/s', relative_uncertainty=0.013)
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# raises ValueError: Uncertainties must be positive.
# expected ValueError: Source calibration strength must be positive.
# TODO FAIL
try:
    cf = Cf()
    cf.calibration_strength = Magnitude(value=5.471E+08, unit='s', relative_uncertainty=0.013)
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# OK raises ValueError: Source calibration_strength units must be standard.
try:
    cf = Cf()
    cf.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=-0.013)
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# OK raises ValueError: Uncertainties must be positive.
cf = Cf()
cf.calibration_strength = Magnitude(value=5.471E+07, unit='1/s', relative_uncertainty=0.013)
print(cf.calibration_strength)
print(f'54710000.0 ± {5.471E+07 * 0.013} 1/s (1.3%)')
# OK
cf = Cf()
cf.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.02)
print(cf.calibration_strength)
print(f'54710000.0 ± {5.471E+07 * 0.02} 1/s (2.0%)')

# 4.3. Assigning a negative value to attribute.value
# ----------------------------------------------------------------------------------------------------------------------
try:
    pass
except ValueError as exc:
    print(f'Raised ValueError: {exc}')

try:
    cf = Cf()
    cf.calibration_strength.value = -5.471E+08
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# TODO FAIL: should raise Source calibration strength must be positive
try:
    cf = Cf()
    cf.calibration_strength.units = 's'
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# TODO FAIL: should raise non-standard unit error.
try:
    cf = Cf()
    cf.calibration_strength.relative_uncertainty = -0.013
except ValueError as exc:
    print(f'Raised ValueError: {exc}')
# TODO FAIL: should raise Source calibration strength must be positive
cf = Cf()
cf.calibration_strength.value = 5.471E+07
print(cf.calibration_strength)
print(f'54710000.0 ± {5.471E+07 * 0.013} 1/s (1.3%)')
# TODO FAIL: should recalculate uncertainties
cf = Cf()
cf.calibration_strength.relative_uncertainty = 0.02
print(cf.calibration_strength)
print(f'54710000.0 ± {5.471E+07 * 0.02} 1/s (2.0%)')
# TODO FAIL: should recalculate uncertainties
